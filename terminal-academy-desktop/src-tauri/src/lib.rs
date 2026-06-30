use std::sync::Mutex;
use std::io::{Write, Read};
use portable_pty::{native_pty_system, CommandBuilder, PtySize, MasterPty};
use tauri::{AppHandle, Emitter, State};

struct PtyState {
  master: Mutex<Option<Box<dyn MasterPty + Send>>>,
  writer: Mutex<Option<Box<dyn Write + Send>>>,
}

impl Default for PtyState {
  fn default() -> Self {
    Self {
      master: Mutex::new(None),
      writer: Mutex::new(None),
    }
  }
}

#[tauri::command]
fn spawn_pty(
  app: AppHandle,
  state: State<'_, PtyState>,
) -> Result<(), String> {
  let pty_system = native_pty_system();
  let pair = pty_system
    .openpty(PtySize {
      rows: 24,
      cols: 80,
      pixel_width: 0,
      pixel_height: 0,
    })
    .map_err(|e| e.to_string())?;

  // Check if remote docker container "academy-sandbox" is running via SSH
  let has_docker = std::process::Command::new("ssh")
    .arg("-i")
    .arg("/Users/ank/.ssh/id_ed25519")
    .arg("-o")
    .arg("ConnectTimeout=3")
    .arg("root@89.22.239.107")
    .arg("docker inspect academy-sandbox")
    .output()
    .map(|out| out.status.success())
    .unwrap_or(false);

  let mut cmd = if has_docker {
    let mut c = CommandBuilder::new("ssh");
    c.arg("-t");
    c.arg("-i");
    c.arg("/Users/ank/.ssh/id_ed25519");
    c.arg("root@89.22.239.107");
    c.arg("docker exec -it academy-sandbox /bin/bash");
    c
  } else {
    let shell = if std::path::Path::new("/bin/zsh").exists() {
      "/bin/zsh"
    } else if std::path::Path::new("/bin/bash").exists() {
      "/bin/bash"
    } else {
      "/bin/sh"
    };
    CommandBuilder::new(shell)
  };

  cmd.env("TERM", "xterm-256color");
  
  let _child = pair.slave.spawn_command(cmd).map_err(|e| e.to_string())?;
  
  let mut reader = pair.master.try_clone_reader().map_err(|e| e.to_string())?;
  let writer = pair.master.take_writer().map_err(|e| e.to_string())?;
  
  {
    let mut state_master = state.master.lock().unwrap();
    let mut state_writer = state.writer.lock().unwrap();
    *state_master = Some(pair.master);
    *state_writer = Some(writer);
  }
  
  // Read stdout in a background thread and emit events
  let app_clone = app.clone();
  std::thread::spawn(move || {
    let mut buf = [0u8; 4096];
    loop {
      match reader.read(&mut buf) {
        Ok(0) => break, // EOF
        Ok(n) => {
          let data = String::from_utf8_lossy(&buf[..n]).to_string();
          let _ = app_clone.emit("pty-data", data);
        }
        Err(_) => break,
      }
    }
  });

  Ok(())
}

#[tauri::command]
fn write_pty(
  state: State<'_, PtyState>,
  data: String,
) -> Result<(), String> {
  let mut writer_lock = state.writer.lock().unwrap();
  if let Some(ref mut writer) = *writer_lock {
    writer.write_all(data.as_bytes()).map_err(|e| e.to_string())?;
    writer.flush().map_err(|e| e.to_string())?;
  }
  Ok(())
}

#[tauri::command]
fn resize_pty(
  state: State<'_, PtyState>,
  rows: u16,
  cols: u16,
) -> Result<(), String> {
  let master_lock = state.master.lock().unwrap();
  if let Some(ref master) = *master_lock {
    master
      .resize(PtySize {
        rows,
        cols,
        pixel_width: 0,
        pixel_height: 0,
      })
      .map_err(|e| e.to_string())?;
  }
  Ok(())
}

#[tauri::command]
fn get_docker_status() -> bool {
  std::process::Command::new("ssh")
    .arg("-i")
    .arg("/Users/ank/.ssh/id_ed25519")
    .arg("-o")
    .arg("ConnectTimeout=3")
    .arg("root@89.22.239.107")
    .arg("docker inspect academy-sandbox")
    .output()
    .map(|out| out.status.success())
    .unwrap_or(false)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .manage(PtyState::default())
    .invoke_handler(tauri::generate_handler![spawn_pty, write_pty, resize_pty, get_docker_status])
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }
      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
