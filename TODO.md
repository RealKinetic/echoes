TODOS
=====

- [ ] Core
  - [ ] Standard Logging Pattern
    - [ ] Include default prefix for easier pattern matching
  - [ ] Config System
    - [ ] Memcache based
      - [ ] Locking Mechanism
      - [ ] Filter requests from memcache distrupter
    - [ ] File based (Yaml?)
    - [x] Default in memory
  - [ ] Distribution System
    - [ ] Percent Random
    - [ ] Activity Based (heavy component usage)
- [ ] Datastore
  - [x] Datastore Errors
  - [x] Default config off common error patterns
    - [x] Verify errors are still accurate
    - [x] Add reference to sdk file(s) with errors
  - [ ] Latency spikes
  - [ ] Hot key / entity monitoring
  - [ ] Entity type pattern matching
  - [ ] Key pattern matching
- [ ] Taskqueues
- [ ] Memcache
  - [ ] Memcache Errors
  - [ ] Default config off common error patterns
  - [ ] Latency spikes
  - [ ] Memcache key clear
    - [ ] Full wipe
    - [ ] Random wipe
  - [ ] Filter config requests from memcache distrupter
  - [ ] Key pattern matching
- [ ] Urlfetch
  - [ ] Memcache Errors
  - [ ] Default config off common error patterns
  - [ ] Latency spikes
  - [ ] Url pattern matching

### Potentials 

  - [ ] Lineage Fault Inject
  - [ ] Tracing integration
  - [ ] Stackdriver / Monitoring integration
