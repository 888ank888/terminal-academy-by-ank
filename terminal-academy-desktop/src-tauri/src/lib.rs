use std::sync::Mutex;
use std::io::{Write, Read};
use portable_pty::{native_pty_system, CommandBuilder, PtySize, MasterPty};
use tauri::{AppHandle, Emitter, State, Manager};

struct PtyState {
  master: Mutex<Option<Box<dyn MasterPty + Send>>>,
  writer: Mutex<Option<Box<dyn Write + Send>>>,
  container_number: Mutex<Option<u32>>,
}

impl Default for PtyState {
  fn default() -> Self {
    Self {
      master: Mutex::new(None),
      writer: Mutex::new(None),
      container_number: Mutex::new(None),
    }
  }
}

// Scans active remote containers to find the smallest available positive index (e.g. academy-sandbox-1)
fn allocate_container_number() -> u32 {
  let output = std::process::Command::new("ssh")
    .arg("-i")
    .arg("/Users/ank/.ssh/id_ed25519")
    .arg("-o")
    .arg("ConnectTimeout=3")
    .arg("root@89.22.239.107")
    .arg("docker ps -a --filter name=academy-sandbox- --format {{.Names}}")
    .output();

  let mut active_indices = Vec::new();

  if let Ok(out) = output {
    let stdout_str = String::from_utf8_lossy(&out.stdout);
    for line in stdout_str.lines() {
      let name = line.trim();
      if name.starts_with("academy-sandbox-") {
        let suffix = &name["academy-sandbox-".len()..];
        if let Ok(num) = suffix.parse::<u32>() {
          active_indices.push(num);
        }
      }
    }
  }

  let mut candidate = 1;
  while active_indices.contains(&candidate) {
    candidate += 1;
  }
  candidate
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

  // Allocate container number sequentially and save it
  let num = allocate_container_number();
  {
    let mut state_num = state.container_number.lock().unwrap();
    *state_num = Some(num);
  }

  let container_name = format!("academy-sandbox-{}", num);

  // Pre-create/run the container remotely if not exists, limit resource and map network, using standard --rm for auto-cleanup
  let _ = std::process::Command::new("ssh")
    .arg("-i")
    .arg("/Users/ank/.ssh/id_ed25519")
    .arg("-o")
    .arg("ConnectTimeout=5")
    .arg("root@89.22.239.107")
    .arg(format!(
      "docker run -d --name {} --network terminal-academy-by-ank_sandbox-network --memory 512m --cpus 0.25 --rm terminal-academy/sandbox:latest sleep infinity",
      container_name
    ))
    .output();

  // Check if remote container is successfully active
  let has_docker = std::process::Command::new("ssh")
    .arg("-i")
    .arg("/Users/ank/.ssh/id_ed25519")
    .arg("-o")
    .arg("ConnectTimeout=3")
    .arg("root@89.22.239.107")
    .arg(format!("docker inspect {}", container_name))
    .output()
    .map(|out| out.status.success())
    .unwrap_or(false);

  let mut cmd = if has_docker {
    let mut c = CommandBuilder::new("ssh");
    c.arg("-t");
    c.arg("-i");
    c.arg("/Users/ank/.ssh/id_ed25519");
    c.arg("root@89.22.239.107");
    c.arg(format!("docker exec -it {} /bin/bash", container_name));
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
fn get_docker_status(state: State<'_, PtyState>) -> bool {
  let num_opt = state.container_number.lock().unwrap().clone();
  if let Some(num) = num_opt {
    let container_name = format!("academy-sandbox-{}", num);
    std::process::Command::new("ssh")
      .arg("-i")
      .arg("/Users/ank/.ssh/id_ed25519")
      .arg("-o")
      .arg("ConnectTimeout=3")
      .arg("root@89.22.239.107")
      .arg(format!("docker inspect {}", container_name))
      .output()
      .map(|out| out.status.success())
      .unwrap_or(false)
  } else {
    false
  }
}

#[tauri::command]
fn destroy_sandbox(state: State<'_, PtyState>) -> Result<(), String> {
  let num_opt = state.container_number.lock().unwrap().clone();
  if let Some(num) = num_opt {
    let container_name = format!("academy-sandbox-{}", num);
    let _ = std::process::Command::new("ssh")
      .arg("-i")
      .arg("/Users/ank/.ssh/id_ed25519")
      .arg("-o")
      .arg("ConnectTimeout=5")
      .arg("root@89.22.239.107")
      .arg(format!("docker stop {}", container_name))
      .output();
  }
  Ok(())
}

#[tauri::command]
fn reset_sandbox(state: State<'_, PtyState>) -> Result<(), String> {
  let num_opt = state.container_number.lock().unwrap().clone();
  if let Some(num) = num_opt {
    let container_name = format!("academy-sandbox-{}", num);
    let _ = std::process::Command::new("ssh")
      .arg("-i")
      .arg("/Users/ank/.ssh/id_ed25519")
      .arg("-o")
      .arg("ConnectTimeout=5")
      .arg("root@89.22.239.107")
      .arg(format!("docker stop {}", container_name))
      .output();
    let _ = std::process::Command::new("ssh")
      .arg("-i")
      .arg("/Users/ank/.ssh/id_ed25519")
      .arg("-o")
      .arg("ConnectTimeout=5")
      .arg("root@89.22.239.107")
      .arg(format!(
        "docker run -d --name {} --network terminal-academy-by-ank_sandbox-network --memory 512m --cpus 0.25 --rm terminal-academy/sandbox:latest sleep infinity",
        container_name
      ))
      .output();
  }
  Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .manage(PtyState::default())
    .invoke_handler(tauri::generate_handler![spawn_pty, write_pty, resize_pty, get_docker_status, destroy_sandbox, reset_sandbox])
    .on_window_event(|window, event| {
      if let tauri::WindowEvent::Destroyed = event {
        let num_opt = {
          let state = window.state::<PtyState>();
          let x = state.container_number.lock().unwrap().clone();
          x
        };
        if let Some(num) = num_opt {
          let container_name = format!("academy-sandbox-{}", num);
          let _ = std::process::Command::new("ssh")
            .arg("-i")
            .arg("/Users/ank/.ssh/id_ed25519")
            .arg("-o")
            .arg("ConnectTimeout=5")
            .arg("root@89.22.239.107")
            .arg(format!("docker stop {}", container_name))
            .output();
        }
      }
    })
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
