# Terminal Academy Skill Tree: DevOps & Containers

Welcome to the **DevOps & Containers** branch of the Terminal Academy Skill Tree. This path takes you from basic container execution through complex CI/CD pipelines and up to managing distributed systems in Kubernetes.

Each node contains 14 practical troubleshooting incidents and 1 Boss Fight. Theory is left at the door; prepare to fix broken pipelines, debug crashing containers, and secure exposed clusters.

---

## Node 1: Docker Fundamentals
- **Dependencies:** Linux CLI Basics
- **Description:** Core Docker engine interaction, container lifecycle, and basic execution. Focus on fixing fundamental operational errors.

### Incidents
1. **Ghost Container:** A background container is holding a lock on a file. Identify its ID and forcibly stop it.
2. **Port Clash:** An Nginx container fails to start because the host's port 80 is occupied. Find the conflicting process or re-bind the container to 8080.
3. **Silent Crash:** A Node.js container exits immediately. Extract the stack trace from the closed container's logs to find the missing environment variable.
4. **Interactive Rescue:** An Alpine container executes its script and dies. Override the entrypoint to `/bin/sh` to inspect its filesystem.
5. **Dangling Process:** A container is stuck in "Removal In Progress". Identify and kill the underlying containerd shim process.
6. **Name Conflict:** A deployment script fails because `db_main` already exists. Rename the old container to `db_main_legacy` and deploy the new one.
7. **Environment Missing:** A Python API throws a connection error. Start the container passing the correct `DATABASE_URL` via environment variables.
8. **Zombie PID 1:** A container's main process is dead but the container is still running. Investigate the PID 1 lifecycle issue and send a SIGKILL.
9. **Detached Chaos:** 50 unnamed, exited containers are clogging the system. Write a command to bulk-remove all exited containers without touching running ones.
10. **Data Extraction:** A container generated an SSL cert before crashing. Use `docker cp` to extract the cert from the stopped container.
11. **Hot Patching:** Inject a patched binary into a running container and restart the internal service without stopping the container.
12. **Exec Challenge:** Run a `pg_dump` command inside an already running PostgreSQL container and pipe the output to the host.
13. **Architecture Mismatch:** A pulled image fails to run on an ARM host. Pull and run the specific `linux/amd64` platform image using QEMU emulation.
14. **Inspection Duty:** Parse the `docker inspect` JSON output using `jq` to find a container's exact IP address on the Docker bridge.
15. **BOSS FIGHT: The Cleanup:** A chaotic environment with multiple crashing containers, port conflicts, and dangling images. Clean the environment, extract a decryption key from a crashing container, and successfully launch the final application container with specific injected variables and ports.

---

## Node 2: Docker Images & Build Context
- **Dependencies:** Node 1
- **Description:** Crafting Dockerfiles, understanding layers, caching, and optimizing the build context.

### Incidents
1. **Missing Base:** A build fails because the base image tag `ubuntu:23.10-custom` doesn't exist. Update the Dockerfile to a valid LTS tag.
2. **Context Bloat:** A build takes 10 minutes to send the build context. Create a `.dockerignore` to exclude the 5GB `node_modules` and `.git` folders.
3. **Cache Busting:** A script in the Dockerfile is using a stale cached version. Reorder the `RUN` and `COPY` directives to optimize caching.
4. **Permission Denied:** A built image fails to execute its entrypoint. Fix the Dockerfile to `chmod +x` the script before execution.
5. **Apt Cache Bloat:** An image is 500MB larger than it should be. Add `apt-get clean` and `rm -rf /var/lib/apt/lists/*` to the package installation layer.
6. **CMD vs ENTRYPOINT:** A container ignores CLI arguments. Convert the Dockerfile's `CMD` to an `ENTRYPOINT` array so arguments append correctly.
7. **Orphaned Dependencies:** A build fails because a `RUN make` step lacks build-essential. Add the dependency and clean it up in the same layer.
8. **Timezone Hang:** A build gets stuck on `tzdata` interactive prompt. Set `DEBIAN_FRONTEND=noninteractive` to fix it.
9. **Bad Symlink:** An image is missing a required symlink. Fix the relative path in the `RUN ln -s` command within the Dockerfile.
10. **Build Arg Failure:** A build requires an API key but it's hardcoded. Parameterize it using `ARG` and pass it during `docker build`.
11. **Expose Ignored:** An application runs but cannot be reached. Realize `EXPOSE` is documentation; modify the `docker run` command to actually publish the port.
12. **Zombie Layers:** A developer created 15 layers of `RUN echo`. Consolidate them into a single `RUN` instruction with `&&`.
13. **Platform Build:** Cross-compile an image for `linux/arm64` on an `amd64` host using `buildx`.
14. **Corrupt Image:** An image pull was interrupted. Identify the corrupted layer and clear the local docker builder cache.
15. **BOSS FIGHT: The Monolith:** You are given a massive 4GB Dockerfile that takes 20 minutes to build and fails at step 45. Optimize the build context, fix the dependency errors, implement proper layer caching, and reduce the final image size to under 300MB.

---

## Node 3: Docker Volumes & Persistent Data
- **Dependencies:** Node 1
- **Description:** Managing stateful containers, bind mounts, named volumes, and permission issues.

### Incidents
1. **Lost State:** A MySQL container restarts and all data is lost. Re-launch it with a named volume attached to `/var/lib/mysql`.
2. **Bind Mount Denied:** A bind mount fails on a SELinux/AppArmor enabled host. Append the `:z` or `:Z` flag to the mount command.
3. **Read-Only Crash:** A web app crashes because its config mount is read-only but it tries to write logs there. Split the mounts: RO for config, RW for logs.
4. **Volume Orphan:** Identify and remove 20 dangling named volumes that are eating up 100GB of host disk space.
5. **UID/GID Mismatch:** A containerized app runs as user `1001` but the host directory is owned by `root`. Fix the host directory permissions to match the container.
6. **Data Injection:** Pre-populate a named volume with an initial database dump by running a temporary container.
7. **Volume Backup:** Create a tarball backup of a named volume using a lightweight busybox container.
8. **Volume Restore:** Restore a tarball backup into a new named volume and attach it to a recovery container.
9. **Mount Obscuring:** A developer mounted a host directory over `/app/libs`, hiding the built-in libraries. Change the mount point to `/app/custom_libs`.
10. **NFS Mount Failure:** A container fails to start because its volume driver is trying to reach a dead NFS server. Remove the volume and recreate it with correct NFS opts.
11. **Tmpfs Bypass:** An app writes sensitive keys to disk. Mount a `tmpfs` at `/app/secrets` so data stays in RAM.
12. **Shared State:** Two containers need to read/write the same files. Create a shared named volume and mount it to both, resolving a file lock issue.
13. **Stale Socket:** A containerized daemon fails because an old `.sock` file exists in a persistent volume. Write a wrapper script to remove the socket on startup.
14. **Inode Exhaustion:** A volume runs out of inodes due to millions of session files. Identify the issue and clear the files.
15. **BOSS FIGHT: State Recovery:** A database container was accidentally deleted. The named volume still exists but has corrupted permissions and an old lock file. Fix the permissions, clear the lock, backup the data, and successfully restore the database in a new container without data loss.

---

## Node 4: Docker Networking
- **Dependencies:** Node 1
- **Description:** Bridge networks, custom routing, DNS resolution, and container-to-container communication.

### Incidents
1. **Default Bridge Isolation:** Two containers on the default bridge cannot resolve each other by name. Create a custom network and connect both to enable DNS.
2. **IP Conflict:** A custom network creation fails because the subnet overlaps with the host's VPN. Recreate the network with a specific `--subnet`.
3. **Hidden Port:** A web container cannot reach the database container. Inspect the network and realize the DB is listening on localhost instead of `0.0.0.0`.
4. **Macvlan Chaos:** A container on a macvlan network cannot ping the host. Configure a virtual macvlan interface on the host to bridge the communication.
5. **Legacy Linking:** A legacy container uses `--link`. Migrate it to a custom bridge network and update the application to use DNS.
6. **Host Network Hijack:** A container running with `--network host` is conflicting with the host's SSH daemon. Reconfigure the container to use a bridge and mapped ports.
7. **DNS Timeout:** A container cannot reach the internet because it inherited a bad `/etc/resolv.conf`. Run the container with `--dns 8.8.8.8`.
8. **Routing Loop:** A containerized VPN creates a default route that breaks Docker's internal routing. Manually manipulate the container's `ip route` table.
9. **Expose vs Publish:** A developer used `EXPOSE 80` but the port is inaccessible. Differentiate between expose and publish, and use `-p 8080:80`.
10. **Hairpin NAT Failure:** A container cannot reach its own public IP. Implement a workaround using internal DNS aliases.
11. **Network Disconnect:** A running container needs to be moved from the `frontend` network to the `backend` network with zero downtime. Use `docker network connect/disconnect`.
12. **MTU Mismatch:** Packets are dropping between containers due to an MTU mismatch with the host interface. Create a network with the correct MTU option.
13. **Iptables Bypass:** Docker bypassed the host's UFW firewall, exposing a database. Configure `DOCKER-USER` iptables chain to block external access.
14. **Overlay Intro:** A local swarm container cannot reach another. Troubleshoot the overlay network's VXLAN port (4789) firewall issue.
15. **BOSS FIGHT: The Network Maze:** Three tiers of containers (web, api, db) are misconfigured. Web cannot see API, API cannot resolve DB, and DB is accidentally exposed to the public internet. Redesign the networks, fix the DNS, secure the DB, and establish end-to-end communication.

---

## Node 5: Docker Compose Fundamentals
- **Dependencies:** Node 2, Node 3, Node 4
- **Description:** Multi-container orchestration, YAML syntax, service dependencies, and environment files.

### Incidents
1. **YAML Indentation:** `docker-compose up` fails due to a mapping error. Fix the misaligned `ports` array in the YAML file.
2. **Version Mismatch:** A v3 Compose file uses a v2 feature (`condition: service_healthy`). Upgrade the schema and implement the correct healthcheck syntax.
3. **Circular Dependency:** `web` depends on `api`, which depends on `db`, which depends on `web`. Break the loop to allow the stack to start.
4. **Ghost Variables:** A compose file references `${API_KEY}` but it's empty. Create a `.env` file and ensure Compose reads it.
5. **Volume Path Error:** A relative bind mount `./data:/data` fails because the Compose file was executed from a different directory. Fix context paths.
6. **Port Collision:** Two services in the same Compose file try to bind to host port 80. Map them to 8081 and 8082.
7. **Orphaned Containers:** A service was renamed from `redis` to `cache`, but `docker-compose up` leaves the old `redis` running. Use `--remove-orphans`.
8. **Build vs Image:** A service has both `build:` and `image:` defined but pulls an old image. Force a rebuild with `docker-compose build`.
9. **Command Override:** The default image command crashes. Use the `command:` directive in Compose to run a sleep loop for debugging.
10. **Network Isolation:** The `admin` service cannot reach the `db` service. Place them on the same custom Compose network.
11. **Startup Race Condition:** The `api` crashes because `db` is up but PostgreSQL isn't ready. Implement a `wait-for-it.sh` script or a proper `depends_on` healthcheck.
12. **Env File Precedence:** An environment variable is defined in both `.env` and `environment:`. Determine the precedence and fix the conflicting value.
13. **Compose Down Hang:** `docker-compose down` hangs forever. Identify the container ignoring SIGTERM and configure `stop_grace_period`.
14. **Scaling Failure:** `docker-compose up --scale web=3` fails due to a static host port mapping. Change the port mapping to ephemeral (`- "80"`).
15. **BOSS FIGHT: Stack Resurrection:** An entire microservice stack YAML is corrupted. Fix syntax errors, resolve dependency loops, configure proper networks, implement database healthchecks, and successfully bring up the 5-service stack without race conditions.

---

## Node 6: Advanced Docker Compose
- **Dependencies:** Node 5
- **Description:** Profiles, overrides, extending services, and complex deployment topologies.

### Incidents
1. **Profile Activation:** A `debug` service isn't starting. Run compose with the correct `--profile` flag to activate it.
2. **Override Collision:** `docker-compose.override.yml` is breaking the production setup. Understand how Compose merges files and fix the port bindings.
3. **Extension Hell:** A service using `extends` fails because it references a missing file. Fix the path in the `file:` directive.
4. **Multiple Compose Files:** Merge three different compose files (`base.yml`, `dev.yml`, `metrics.yml`) into a single execution command.
5. **Fragmented Networks:** A service needs to join an external network created outside of Compose. Configure `external: true` for the network.
6. **Resource Limits:** A runaway container freezes the host. Add `deploy.resources` to the Compose file to limit CPU and Memory.
7. **Logging Driver:** A container generates too many logs. Configure the `json-file` logging driver in Compose to rotate max 3 files of 10MB.
8. **Init Process:** A Node.js app doesn't reap zombie processes. Add `init: true` to the service definition.
9. **Secrets Management:** A password is in plain text. Migrate it to use Compose `secrets:` and modify the app to read from `/run/secrets/`.
10. **Healthcheck Loop:** A healthcheck fails because it lacks `curl`. Change the test to use `wget` or a native language script.
11. **Scale Down Race:** Scaling down drops active connections. Implement a pre-stop script handling SIGTERM gracefully.
12. **Context Subdirectories:** A service needs to build from a sibling directory, but cannot access files outside its context. Adjust the `build.context` and `build.dockerfile` paths.
13. **Variable Interpolation:** A literal `$` in a password is being interpolated as an empty variable. Escape it using `$$`.
14. **Custom Project Name:** Two branches of the same repo are spinning up Compose and clashing names. Use `-p` or `COMPOSE_PROJECT_NAME` to isolate them.
15. **BOSS FIGHT: The Environment Matrix:** Manage a complex application that requires dev, staging, and prod configurations. Using a base compose file and multiple overrides/profiles, launch all three environments on the same host without port collisions, ensuring prod uses secrets and dev uses local bind mounts.

---

## Node 7: Multi-Stage & Optimized Builds
- **Dependencies:** Node 2
- **Description:** Advanced Dockerfile techniques, reducing attack surface, optimizing build times, and scratch containers.

### Incidents
1. **Stage Bleed:** A multi-stage build still includes the Go compiler. Fix the `COPY --from=builder` path to only copy the binary.
2. **Missing Libc:** A dynamically linked C binary panics in an `alpine` stage. Switch to a statically linked build or use a `glibc` base.
3. **Scratch Panic:** A Go binary in a `scratch` container fails to make HTTPS requests due to missing root certificates. Copy `ca-certificates` from the builder stage.
4. **Scratch User:** A scratch container runs as root. Copy `/etc/passwd` from the builder and set `USER nonroot`.
5. **Asset Pipeline:** A Node.js build stage generates static files, but the Nginx stage can't find them. Correct the destination path in the `COPY --from`.
6. **Build Cache Invalidation:** A change to README.md invalidates the `npm install` cache. Move the `COPY README.md` command after the install steps.
7. **Target Stage:** A Dockerfile has `dev`, `test`, and `prod` stages. Run a build targeting only the `test` stage to run unit tests.
8. **Secret Leak:** A build uses an SSH key via `COPY`, leaking it into the layer. Refactor to use BuildKit `--mount=type=ssh`.
9. **Cache Mount:** `pip install` is downloading packages every time. Implement `--mount=type=cache` to cache the pip directory between builds.
10. **Arg Scoping:** An `ARG` defined before `FROM` is not available inside the build stage. Redeclare the `ARG` inside the stage.
11. **Huge Layer:** A `RUN` command downloads a zip, extracts it, and deletes the zip, but the image is still large. Chain the commands in one layer.
12. **Python Bytecode Bloat:** Python creates `.pyc` files during build. Set `PYTHONDONTWRITEBYTECODE=1` to save space.
13. **Distroless Debugging:** A distroless container crashes and has no shell. Use `docker run -ti --entrypoint sh <image>:debug` using the debug tag.
14. **Multi-Architecture:** Configure a Dockerfile to use the `$TARGETARCH` automatic build arg to download the correct binary architecture.
15. **BOSS FIGHT: The Micro-Image:** You are handed a 1.2GB Java/Node hybrid Dockerfile. Convert it into a 3-stage build (Node for frontend, Maven for backend, JRE for runtime), utilize BuildKit cache mounts, secure it as a non-root user, and produce a final image under 150MB.

---

## Node 8: Container Security & Hardening
- **Dependencies:** Node 7
- **Description:** Linux capabilities, read-only filesystems, rootless Docker, and privilege escalation prevention.

### Incidents
1. **Root Escalation:** A container runs as root and mounts `/var/run/docker.sock`. Identify the vulnerability and remove the socket mount.
2. **Capability Drop:** A web server doesn't need root capabilities. Run the container with `--cap-drop=ALL` and only add back `NET_BIND_SERVICE`.
3. **Privileged Mode:** A container is running with `--privileged`. Determine what specific capability it actually needs (`SYS_ADMIN`) and restrict it.
4. **Read-Only Rootfs:** Run a container with `--read-only`. Fix the subsequent crash by mounting a `tmpfs` to `/tmp` and `/var/run`.
5. **User Namespace Mapping:** A container creates files as root that are undeletable by the host user. Configure User Namespaces (`userns-remap`) in the Docker daemon.
6. **No-New-Privileges:** Prevent a compromised container process from using `sudo` or `su` by enforcing `--security-opt=no-new-privileges:true`.
7. **AppArmor Profile:** A container is writing to `/etc`. Apply a custom AppArmor profile to deny writes to sensitive host paths.
8. **Seccomp Violation:** A container crashes because it tries to call a blocked syscall (`ptrace`). Identify the block via audit logs and run with a custom seccomp profile.
9. **Image Scanning:** Run `trivy` against an image, identify a critical CVE in `openssl`, and update the base image to patch it.
10. **Secret Environment Leak:** A container passes DB credentials via `docker run -e`. Extract the secret via `docker inspect` to prove it's insecure, then switch to Docker Secrets / file mounts.
11. **PIDs Cgroup:** A fork-bomb in a container freezes the host. Apply `--pids-limit=100` to prevent process exhaustion.
12. **Rootless Daemon:** The Docker daemon is running as root. Reconfigure the host to run rootless Docker for a specific user.
13. **Arbitrary Execution:** An attacker gained RCE and downloaded malware. Prevent this by removing `curl` and `wget` from the final image stage.
14. **Host PID Namespace:** A container is started with `--pid=host` and is killing host processes. Isolate it back to its own PID namespace.
15. **BOSS FIGHT: The Hardened Bunker:** Take a vulnerable, overly privileged, root-running web application and fully harden it. Implement read-only rootfs, drop all capabilities, run as a non-root user, limit PIDs/Memory, apply a strict seccomp profile, and prove the app still functions while being impervious to a simulated breakout script.

---

## Node 9: Docker Registries & Image Management
- **Dependencies:** Node 2
- **Description:** Private registries, tagging strategies, authentication, and image garbage collection.

### Incidents
1. **Pull Rate Limit:** Anonymous Docker Hub pulls are rate-limited. Authenticate using `docker login` with a personal access token.
2. **Tag Overwrite:** Production broke because `latest` was overwritten. Implement semantic versioning tagging (`v1.2.3`) and pull the specific tag.
3. **Insecure Registry:** A push to a local registry (`http://registry:5000`) fails. Configure the Docker daemon's `insecure-registries` to allow it.
4. **Auth Expiration:** `docker push` fails with a 401. Refresh the AWS ECR login token and retry the push.
5. **Manifest Unknown:** Pulling an image fails because the manifest is missing for the current architecture. Use `docker manifest inspect` to verify available architectures.
6. **Garbage Collection:** A private registry is out of disk space. Run the registry's garbage collection routine to delete untagged blobs.
7. **Local Registry Setup:** Deploy a local Docker registry with basic HTpasswd authentication and test pushing an image.
8. **Dangling Images:** The host is out of disk space. Prune dangling images, build cache, and unused networks using `docker system prune`.
9. **Mirror Configuration:** Configure the Docker daemon to use a pull-through cache registry mirror to speed up builds.
10. **Image Save/Load:** Move an image from an air-gapped machine to another using `docker save` and `docker load`.
11. **Content Trust:** Enforce `DOCKER_CONTENT_TRUST=1` and sign an image using Notary before pushing it.
12. **Stale Pull:** A container restarts but uses the old `latest` image. Force a `docker pull` before `docker run`.
13. **Registry Sync:** Write a script to pull an image from Docker Hub, re-tag it, and push it to a private AWS ECR registry.
14. **Blob Corruption:** A registry complains about a corrupted layer blob. Delete the layer from the backend storage and force a re-push.
15. **BOSS FIGHT: The Air-Gapped Migration:** You have 5 critical images on a public registry. You must deploy a secure, authenticated local registry on an isolated network, script the download and transfer of the images via tarballs, load them, push them to the local registry, and reconfigure the isolated cluster to pull from it successfully.

---

## Node 10: CI/CD Fundamentals
- **Dependencies:** Node 5
- **Description:** Introduction to continuous integration, runner registration, automated testing, and basic YAML pipelines.

### Incidents
1. **Syntax Error:** A GitHub Actions/GitLab CI YAML file has a syntax error. Validate and fix the bad indentation.
2. **Runner Offline:** A pipeline is stuck in "Pending". Troubleshoot the self-hosted runner service and restart it.
3. **Secret Exposure:** A pipeline prints a database password in the build logs. Mask the variable in the CI settings.
4. **Wrong Trigger:** A pipeline runs on every markdown edit. Restrict the trigger to `push` events on the `main` branch affecting the `src/` directory.
5. **Missing Dependency:** A build job fails because `make` is not installed on the CI runner. Add the installation step to the pipeline.
6. **Failing Fast:** A pipeline continues running a 10-minute deployment even if the tests fail. Configure the job dependencies so `deploy` requires `test`.
7. **Permissions Denied:** A script in the repo cannot be executed by the CI runner. Add a `chmod +x` step before execution.
8. **Workspace Dirty:** A runner fails a job because old files from a previous run are conflicting. Add a cleanup/checkout step to reset the workspace.
9. **Environment Variable Missing:** A build requires `NODE_ENV=production`. Inject the variable into the CI job environment.
10. **Timeout Reached:** A build hangs indefinitely on a user prompt. Set a job timeout of 5 minutes and add `--non-interactive` flags.
11. **Artifact Loss:** A compiled binary is needed in the next job but is lost. Upload the binary as a CI artifact and download it in the next job.
12. **Service Container Failure:** A test job requires Redis. Configure a Redis service container within the CI YAML.
13. **Bad Exit Code:** A test suite fails but the CI job passes. Fix the shell script so it returns a non-zero exit code on failure.
14. **Matrix Build:** A library needs testing on Python 3.8, 3.9, and 3.10. Convert a single job into a matrix build.
15. **BOSS FIGHT: The Broken Pipeline:** You inherit a red CI pipeline. The runner is disconnected, tests use hardcoded local paths, secrets are exposed, and jobs run out of order. Register the runner, secure the secrets, fix the job dependencies, implement service containers for tests, and achieve a green build.

---

## Node 11: CI/CD Pipeline Optimization
- **Dependencies:** Node 10
- **Description:** Caching dependencies, parallel execution, building containers in CI, and reducing pipeline execution time.

### Incidents
1. **Cache Miss:** NPM dependencies are downloaded every run. Implement directory caching using hash files (e.g., `package-lock.json`) as cache keys.
2. **Cache Bloat:** The CI cache has grown to 10GB, slowing down cache restoration. Implement cache eviction or restrict caching to specific paths.
3. **Docker in Docker (DinD):** A pipeline needs to build a Docker image but the runner lacks the Docker daemon. Configure DinD or mount the docker socket securely.
4. **Slow Image Build:** A Docker build in CI takes 15 minutes. Implement inline registry caching (`--cache-from`) to speed it up.
5. **Concurrent Job Limit:** A matrix build creates 20 jobs and hits API limits. Limit the maximum parallel execution in the matrix strategy.
6. **Redundant Tests:** Tests are running for UI code when only backend code changed. Use path filters to skip the job dynamically.
7. **Artifact Overwrite:** Two matrix jobs upload an artifact with the same name. Parameterize the artifact name with the matrix OS variable.
8. **Stale Cache Poisoning:** A bad dependency got cached and now all builds fail. Manually invalidate the cache key or bump the cache version.
9. **Flaky Tests:** A test fails 10% of the time due to network timeouts. Implement a retry mechanism at the job or step level.
10. **Buildx Setup:** A pipeline needs to build a multi-arch image. Configure `docker buildx` and QEMU within the CI pipeline.
11. **Shallow Clone:** A script requiring full git history fails because CI does a shallow clone. Configure the checkout step to fetch all history (`fetch-depth: 0`).
12. **Wait for Services:** Tests fail because the database container isn't ready. Add a polling script to wait for the DB port to open before running tests.
13. **Merge Queue:** Multiple PRs merge at once, breaking `main`. Configure a merge queue pipeline strategy to serialize tests.
14. **Custom Runner Image:** The default runner lacks tools, adding 3 minutes of `apt-get` steps. Build a custom runner Docker image and use it for the job.
15. **BOSS FIGHT: The 20-Minute Monolith:** A pipeline takes 25 minutes to build, test, and package an application. By implementing dependency caching, Docker layer caching, parallelizing test suites, and using custom runner images, reduce the pipeline execution time to under 4 minutes while maintaining 100% test coverage.

---

## Node 12: Continuous Deployment & Automation
- **Dependencies:** Node 11
- **Description:** Automated deployments, SSH access from CI, atomic deployments, and rollback strategies.

### Incidents
1. **SSH Key Formatting:** CI fails to SSH into the production server. Fix the multi-line private key formatting in the CI secrets.
2. **Strict Host Key Checking:** SSH deployment hangs waiting for fingerprint confirmation. Add the server's public key to `known_hosts` in the CI job.
3. **Atomic Symlinks:** A deployment copies files directly to `/var/www`, causing downtime. Implement a script to deploy to a timestamped folder and swap a symlink.
4. **Database Migration Fail:** A deployment runs `db:migrate` and crashes, leaving the DB in a bad state. Implement a pre-deployment backup and rollback step.
5. **Zero Downtime Reload:** Nginx is restarted during deployment, dropping connections. Change the script to use `nginx -s reload` instead.
6. **Blue-Green Toggle:** You have active `blue` and idle `green` environments. Update the load balancer config via script to route traffic to `green`.
7. **Deployment Triggers:** A deployment ran on a feature branch. Restrict the deployment job to only run when a Git tag matching `v*` is pushed.
8. **Registry Webhook:** Configure a Docker Registry webhook to trigger a deployment script on the target server automatically upon image push.
9. **Configuration Drift:** The CI pipeline deploys an old config file. Separate the config from the codebase and deploy it via a dedicated configuration management step.
10. **Canary Analysis:** A script needs to verify a deployment before switching full traffic. Write a curl script that checks a health endpoint 5 times before succeeding.
11. **Rollback Trigger:** A deployment fails the healthcheck. Catch the failure exit code and execute a script that reverts the image tag and restarts the service.
12. **Rate Limit Hit:** A script pulling an image during deployment hits Docker Hub limits. Authenticate the target server's Docker daemon.
13. **Zombie Processes:** A deployed background worker isn't stopped before the new one starts, causing duplicate data. Fix the systemd service to send SIGTERM correctly.
14. **Approval Gate:** Production deployments are happening automatically. Insert a manual approval gate in the pipeline before the deploy job executes.
15. **BOSS FIGHT: The Flawless Cutover:** Set up a full CD pipeline that authenticates via SSH, deploys a new Docker container alongside the old one, runs database migrations, executes a health check, dynamically switches the Nginx upstream via configuration reload, and automatically rolls back if the health check fails—all with zero dropped requests.

---

## Node 13: Introduction to Kubernetes (k3s/minikube)
- **Dependencies:** Node 5
- **Description:** Kubeconfig, API interaction, namespaces, basic Pods, and translating Docker concepts to K8s.

### Incidents
1. **Context Confusion:** `kubectl` is pointing to the wrong cluster. Switch the kubernetes context to the local `minikube` or `k3d` cluster.
2. **API Server Down:** `kubectl get pods` times out. Check the local container runtime to ensure the minikube/k3s master node container is running.
3. **Namespace Isolation:** A pod cannot be found. Realize it was deployed in the `dev` namespace; append `-n dev` to your command.
4. **Pod Creation Syntax:** An imperative command `kubectl run` fails. Correct the syntax to create an Nginx pod on port 80.
5. **CrashLoopBackOff:** A newly created pod crashes repeatedly. Use `kubectl logs` and `kubectl describe` to identify a missing start command.
6. **ImagePullBackOff:** A pod fails to start because it can't find a local image. Load the local Docker image into the k3d/minikube cluster registry.
7. **Port Forwarding:** A database pod is running but inaccessible from the host. Use `kubectl port-forward` to map local port 5432 to the pod.
8. **Interactive Exec:** Drop into a shell inside a running pod using `kubectl exec -it <pod> -- /bin/sh`.
9. **Label Selectors:** Delete 5 specific pods out of 20 by using a label selector (`kubectl delete pods -l app=frontend`).
10. **Resource Deletion:** A pod stuck in `Terminating` state for 10 minutes. Force delete it with `--grace-period=0 --force`.
11. **YAML Export:** You need the YAML of a running imperative pod. Use `kubectl get pod <name> -o yaml > pod.yml` and strip the cluster-specific metadata.
12. **Dry Run Validation:** Validate a pod YAML file without creating it using `--dry-run=client`.
13. **Multi-Container Pod:** A pod has two containers. View the logs of the specific sidecar container using the `-c` flag.
14. **Node Readiness:** A pod is `Pending`. Check `kubectl get nodes` and find the node has a `DiskPressure` taint. Free up disk space.
15. **BOSS FIGHT: The Cluster Bootstrap:** You are given an empty cluster and a set of Docker run commands. Translate them into Kubernetes Pod YAML manifests, deploy them into specific namespaces, handle local image loading, set up port-forwards, and prove the application is accessible from your host machine.

---

## Node 14: Kubernetes Deployments & ReplicaSets
- **Dependencies:** Node 13
- **Description:** Declarative state, scaling, self-healing, and rolling updates.

### Incidents
1. **Replica Mismatch:** A Deployment specifies 3 replicas but only 1 is running. Check node capacity and scaling limits.
2. **Selector Chaos:** A Deployment fails to create pods because its `matchLabels` do not match the Pod template labels. Fix the YAML.
3. **Scale Command:** Imperatively scale a deployment named `web-scale` from 2 to 5 replicas to handle a traffic spike.
4. **Rolling Update Hang:** A deployment update is stuck because the new image tag is invalid. Identify the stuck ReplicaSet.
5. **Rollout Undo:** Revert the stuck deployment to the previous stable revision using `kubectl rollout undo`.
6. **Surge Configuration:** An update brings down too many pods at once. Adjust `maxSurge` and `maxUnavailable` in the Deployment strategy.
7. **Orphaned Pods:** A Deployment was deleted but its pods remain. Realize someone used `kubectl delete replicaset --cascade=orphan`. Clean up the pods.
8. **Probes Failure:** A pod starts but never becomes `Ready`. Fix the misconfigured `readinessProbe` pointing to the wrong port.
9. **Liveness Loop:** A `livenessProbe` is too strict, causing the pod to constantly restart under load. Increase the `failureThreshold` and `timeoutSeconds`.
10. **History Limit:** The deployment history is lost after 2 rollouts. Increase `revisionHistoryLimit` in the YAML.
11. **DaemonSet Miss:** A logging agent needs to run on every node. Convert a Deployment YAML into a DaemonSet YAML.
12. **StatefulSet Ordering:** A StatefulSet's pods are starting in parallel, breaking the database cluster. Ensure `podManagementPolicy` is set correctly for ordered readiness.
13. **Init Container Block:** An app pod won't start because its Init Container is stuck waiting for a database. Fix the Init Container's connection string.
14. **HPA Setup:** Configure a HorizontalPodAutoscaler to scale a deployment based on CPU utilization reaching 80%.
15. **BOSS FIGHT: The Rolling Disaster:** A critical production Deployment is failing during a rolling update, dropping traffic, and restarting constantly due to bad liveness probes. Halt the rollout, fix the probes, adjust the surge parameters, apply the fix, and successfully complete a zero-downtime rolling update.

---

## Node 15: Kubernetes Networking & Services
- **Dependencies:** Node 14
- **Description:** ClusterIP, NodePort, LoadBalancers, CoreDNS, and Ingress controllers.

### Incidents
1. **Service Selector Drop:** A ClusterIP service has no endpoints. Fix the Service's `selector` to match the Deployment's labels.
2. **Port Mismatch:** A Service routes to port 8080, but the pod listens on 80. Fix the `targetPort` vs `port` mapping in the Service YAML.
3. **NodePort Exposure:** Convert a ClusterIP service to a NodePort service so it can be accessed from outside the cluster via the node's IP.
4. **CoreDNS Failure:** Pods cannot resolve service names. Restart the CoreDNS deployment in the `kube-system` namespace.
5. **Cross-Namespace DNS:** The `frontend` pod in `default` namespace cannot reach `db` in the `backend` namespace. Use the FQDN `db.backend.svc.cluster.local`.
6. **Endpoints Manual Edit:** A Service without a selector needs to point to an external database. Manually create the `Endpoints` resource mapping to the external IP.
7. **Ingress 404:** An Ingress rule returns 404. Fix the `path` and `pathType` (e.g., `Prefix` vs `Exact`) in the Ingress resource.
8. **Ingress Class Missing:** An Ingress resource is ignored by the controller. Add the correct `ingressClassName` (e.g., `nginx`).
9. **TLS Termination:** Configure an Ingress resource to terminate HTTPS using a Kubernetes Secret containing the TLS certificate.
10. **Network Policy Block:** A pod cannot reach the database because a default-deny NetworkPolicy is active. Create an allow-list NetworkPolicy for the pod's labels.
11. **LoadBalancer Pending:** A LoadBalancer service is stuck in `Pending` on bare metal. Install and configure MetalLB or switch back to NodePort.
12. **Hairpin Routing:** A pod cannot access a LoadBalancer IP that routes back to itself. Verify kubeproxy settings or use internal service names.
13. **Session Affinity:** A legacy web app requires sticky sessions. Configure `sessionAffinity: ClientIP` on the Service.
14. **Ingress Rewrite:** A backend app expects traffic at `/`, but the Ingress path is `/api`. Add a rewrite-target annotation to the Nginx Ingress.
15. **BOSS FIGHT: Network Lockdown:** A multi-tier application is completely unreachable. Fix the broken Services, resolve the cross-namespace DNS issues, configure an Ingress controller with TLS, and enforce strict NetworkPolicies so the DB can only be reached by the API, and the API only by the frontend.

---

## Node 16: Kubernetes Storage & Persistence
- **Dependencies:** Node 14
- **Description:** Volumes, PersistentVolumes (PV), PersistentVolumeClaims (PVC), and StorageClasses.

### Incidents
1. **PVC Pending:** A PVC is stuck in Pending because no StorageClass exists. Create a local path StorageClass or manually provision a PV.
2. **Capacity Mismatch:** A PVC requests 10Gi, but the available PV is 5Gi. Resize the PV or create a new one that satisfies the claim.
3. **Access Mode Conflict:** A Deployment scales to 2 replicas, but the PVC is `ReadWriteOnce`. Change the strategy to `Recreate` or use a `ReadWriteMany` PV (like NFS).
4. **HostPath Permissions:** A pod mounts a `hostPath` but gets Permission Denied. Apply a `securityContext` to the pod with the correct `fsGroup`.
5. **Retain vs Delete:** A PVC is deleted, and the underlying PV data is wiped. Change the PV's `persistentVolumeReclaimPolicy` to `Retain`.
6. **Lost PV Recovery:** A PVC was deleted but the PV is marked `Released` and cannot be bound to a new PVC. Manually clear the `claimRef` from the PV.
7. **SubPath Mounting:** Two containers in a pod need to write to different folders in the same volume. Use `subPath` in the `volumeMounts`.
8. **EmptyDir Exhaustion:** A pod's `emptyDir` volume fills up the node's disk. Add a `sizeLimit` to the `emptyDir` definition.
9. **Dynamic Provisioning Failure:** A cloud StorageClass fails to provision. Check the CSI driver logs and fix the cloud provider credentials.
10. **StatefulSet Storage:** A StatefulSet needs unique storage per pod. Replace the static PVC with a `volumeClaimTemplate`.
11. **Volume Expansion:** A database PVC is 99% full. Edit the PVC to request more storage and verify the CSI driver resizes the filesystem dynamically.
12. **Read-Only Mount:** Mount a persistent volume as read-only to a reporting pod to prevent accidental data modification.
13. **NFS Mount Timeout:** An NFS-backed PV fails to mount. Check network connectivity from the worker node to the NFS server, not just from the master.
14. **Zombie Attachment:** A pod is deleted but the volume remains attached to the node, preventing a new pod from starting on a different node. Force detach the volume via the cloud provider or CSI plugin.
15. **BOSS FIGHT: The Stateful Migration:** A legacy database runs on a single Pod with a `hostPath` volume. You must migrate this to a StatefulSet using dynamically provisioned PVCs, copy the data from the old volume to the new one with zero data loss, and ensure the new setup survives node restarts and pod rescheduling.

---

## Node 17: Kubernetes ConfigMaps & Secrets
- **Dependencies:** Node 14
- **Description:** Decoupling configuration from images, secret management, and environment injection.

### Incidents
1. **Env Var Typo:** A pod crashes because it expects `DB_HOST` but the ConfigMap provides `DATABASE_HOST`. Map the key correctly in `env[].valueFrom`.
2. **Base64 Blunder:** A Secret contains raw text instead of Base64 encoded text, causing application errors. Encode the values correctly before applying.
3. **Stale Config:** A ConfigMap is updated, but the Pod using it as environment variables doesn't reflect the change. Restart the deployment to pick up the new env vars.
4. **File Mount Overwrite:** Mounting a ConfigMap to `/etc/config` hides all other files in that directory. Use `subPath` or mount to a dedicated directory.
5. **Missing Secret:** A pod is stuck in `ContainerCreating` because a referenced Secret doesn't exist. Create the missing Secret.
6. **EnvFrom Collision:** Using `envFrom` loads 50 variables, causing conflicts. Switch to explicitly defining only the required variables.
7. **Opaque vs Docker-Registry:** Pulling from a private registry fails because the `imagePullSecret` was created as type `Opaque`. Recreate it as `kubernetes.io/dockerconfigjson`.
8. **Hot Reloading:** A ConfigMap mounted as a volume updates automatically, but the app doesn't reload. Write a sidecar container that watches the file and sends a SIGHUP to the app.
9. **Secret Decoding:** Retrieve an existing database password from a Kubernetes Secret, decode it from Base64, and use it to log into a DB pod.
10. **Generator Syntax:** Create a ConfigMap from an entire directory of `.properties` files using `kubectl create configmap --from-file`.
11. **Immutable Configs:** Accidental changes to a critical ConfigMap break production. Set `immutable: true` in the ConfigMap YAML.
12. **Projected Volumes:** Combine two ConfigMaps and a Secret into a single volume mount using a `projected` volume configuration.
13. **RBAC Secret Leak:** A service account can read all secrets in a namespace. Restrict the Role to only `get` specific secret names.
14. **External Secrets (Intro):** A secret is hardcoded in Git. Replace it with a placeholder and configure a basic mechanism (or manual process) to sync it from an external vault.
15. **BOSS FIGHT: The Configuration Nightmare:** An application YAML contains hardcoded passwords, environment-specific URLs, and embedded config files. Refactor the deployment entirely: extract URLs to ConfigMaps, passwords to Secrets, mount config files properly without overwriting system directories, and ensure the pods restart successfully in the new state.

---

## Node 18: Helm & Package Management
- **Dependencies:** Node 14
- **Description:** Helm charts, templating, overriding values, and managing third-party deployments.

### Incidents
1. **Release Conflict:** `helm install` fails because a release name already exists. Use `helm upgrade --install` instead.
2. **Values Override:** A generic Helm chart exposes port 80. Use a `values.yaml` file to override the service type to NodePort and port to 8080.
3. **Template Syntax Error:** A custom Helm chart fails to render due to a missing closing `{{ end }}`. Debug using `helm template --debug`.
4. **Stuck Release:** A Helm release is stuck in `pending-upgrade`. Roll back the release using `helm rollback <name> <revision>`.
5. **Dependency Missing:** A chart requires a PostgreSQL subchart, but it's not downloaded. Run `helm dependency update`.
6. **Hook Failure:** A `pre-install` Helm hook job fails, preventing the chart from installing. Inspect the job logs, fix the issue, and retry.
7. **Namespace Creation:** Helm fails to install because the namespace doesn't exist. Use the `--create-namespace` flag.
8. **Orphaned Resources:** A resource was manually deleted via `kubectl`, breaking Helm's state. Force an update or recreate the resource so Helm can manage it again.
9. **Chart Repository:** Add the Bitnami repository, search for a Redis chart, and fetch the `values.yaml` for inspection.
10. **Version Pinning:** A pipeline broke because it used `helm install` without a version, fetching a breaking major update. Pin the `--version`.
11. **Custom Helpers:** A template uses a helper `{{ include "myapp.fullname" . }}` which produces a name longer than 63 characters, failing K8s validation. Truncate the name in `_helpers.tpl`.
12. **Secret Values:** Pass a database password to a Helm release securely without writing it to `values.yaml` using `--set-string`.
13. **Diffing Changes:** Before applying an upgrade, use a Helm diff plugin (or dry-run) to see exactly which K8s resources will be modified.
14. **CRD Management:** A Helm chart fails to install because CRDs already exist. Understand how Helm handles (or ignores) CRD updates and apply them manually.
15. **BOSS FIGHT: The Chart Crafter:** Take a complex application consisting of a Deployment, Service, Ingress, and ConfigMap. Parameterize it into a fully functional Helm chart. Implement helper templates for labels, conditional blocks for creating the Ingress based on a boolean value, and successfully deploy multiple distinct releases of the app into the same cluster using different values files.

---

## Node 19: Kubernetes RBAC & Security Contexts
- **Dependencies:** Node 14
- **Description:** Roles, RoleBindings, ServiceAccounts, and Pod security hardening.

### Incidents
1. **Forbidden Access:** A CI/CD pipeline pod tries to run `kubectl apply` but gets a 403 Forbidden. Create a ServiceAccount and attach it to the pod.
2. **RoleBinding Scope:** A RoleBinding grants access to the `default` namespace, but the user needs access to `dev`. Create the Role and Binding in the correct namespace.
3. **ClusterRole vs Role:** A user needs to list Nodes. Realize a `Role` cannot grant cluster-scoped access; create a `ClusterRole` and `ClusterRoleBinding`.
4. **ServiceAccount Token:** Extract the JWT token from a specific ServiceAccount and use it to authenticate against the K8s API via `curl`.
5. **Privilege Escalation:** A pod is deployed with `allowPrivilegeEscalation: true`. Modify the PodSecurityContext to set it to `false`.
6. **RunAsNonRoot:** A Deployment fails its security policy because it runs as root. Set `runAsUser: 1000` and `runAsNonRoot: true` in the security context.
7. **Default SA Mount:** The `default` ServiceAccount token is automatically mounted into every pod. Disable this via `automountServiceAccountToken: false`.
8. **Network Spoofing:** A pod requires `NET_RAW` to run ping, but it's stripped. Add the specific capability back in the security context without granting full privileges.
9. **Read-Only Filesystem:** Enforce a read-only root filesystem on a pod, then mount `emptyDir` volumes specifically for `/tmp` and `/var/run`.
10. **Aggregated Roles:** Add custom permissions to the default `admin` ClusterRole using aggregation labels.
11. **Subject Typo:** A RoleBinding specifies `kind: User` instead of `kind: ServiceAccount`. Fix the YAML so the bot can authenticate.
12. **API Groups:** A Role grants access to `pods`, but fails on `deployments`. Add the `apps` API group to the Role definition.
13. **Wildcard Danger:** A Role grants `verbs: ["*"]` on `resources: ["*"]`. Scope it down strictly to `get, list, watch` on `pods, logs`.
14. **Seccomp Profile:** Apply the `RuntimeDefault` seccomp profile to a Deployment to restrict malicious system calls.
15. **BOSS FIGHT: The Zero-Trust Namespace:** You are given a namespace full of highly privileged, root-running pods sharing the default ServiceAccount. You must create strict, least-privilege ServiceAccounts for each component, enforce non-root execution, drop all capabilities, implement read-only filesystems, and write exact RBAC Roles allowing the specific pods to only access the API resources they strictly require.

---

## Node 20: Advanced Kubernetes Troubleshooting & Logging
- **Dependencies:** Node 13, 14, 15, 16
- **Description:** Cluster-level debugging, metrics, advanced log aggregation concepts, and deep system analysis.

### Incidents
1. **OOMKilled:** A pod exits with code 137. Check `kubectl describe pod` to confirm OOMKilled and increase the memory `limit`.
2. **CPU Throttling:** An app is painfully slow despite low CPU usage. Realize the CPU `limit` is too low causing CFS throttling. Adjust requests vs limits.
3. **Evicted Pods:** Nodes are tainted with `DiskPressure`, causing pods to be Evicted. Identify the container filling the disk and clean it up.
4. **Zombie Endpoints:** A Service routes to a deleted pod IP. Restart the `kube-controller-manager` or manually delete the stale Endpoints.
5. **Kubelet Crash:** A node transitions to `NotReady`. SSH into the node, check `journalctl -u kubelet`, and fix the misconfigured swap setting.
6. **Log Aggregation:** Pod logs are lost when pods crash. Implement a fluent-bit DaemonSet to forward logs to a central stdout sink for debugging.
7. **Event Sleuthing:** A Deployment is failing silently. Use `kubectl get events --sort-by='.metadata.creationTimestamp'` to find the underlying API errors.
8. **Ephemeral Containers:** A distroless pod is crashing, and you cannot `exec` into it. Inject an ephemeral debug container using `kubectl debug`.
9. **Dangling Network Interfaces:** A node runs out of IPs because CNI interfaces aren't being cleaned up. Manually identify and delete the orphaned `veth` interfaces.
10. **DNS Resolution Loop:** A pod's `/etc/resolv.conf` has a circular reference. Fix the CoreDNS ConfigMap `forward` plugin.
11. **API Rate Limiting:** Controllers are failing because they hit the kube-apiserver rate limit. Identify the rogue script spamming the API and kill it.
12. **Stuck Finalizers:** A namespace is stuck in `Terminating` for days. Remove the dangling finalizers from the remaining resources using `kubectl patch`.
13. **Metrics Server:** `kubectl top pods` fails. Deploy the metrics-server and configure kubelet insecure TLS to make it work locally.
14. **Etcd Desync:** (Simulated) The cluster state is inconsistent. Perform a backup of the etcd database using `etcdctl`.
15. **BOSS FIGHT: The Cluster Meltdown:** A full-scale disaster. Nodes are flapping `NotReady`, the API server is sluggish, pods are Evicted, DNS is failing, and the main application is OOMKilled. You must utilize all debugging tools (`describe`, `logs`, `events`, `top`, `debug` containers, `journalctl` on nodes) to stabilize the control plane, fix the CNI/DNS issues, adjust resource limits to stop the evictions, and bring the cluster back to a healthy, green state.

---
*End of DevOps & Containers Skill Tree.*
