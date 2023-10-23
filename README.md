# Python API client for vo.fai.kz


## Usage
```python
from vokz import Client
client = Client("<your API key>")
```
The API key is available in user profile upon registering at vo.fai.kz.

### Submission status
```python
# Query status of your submissions
status = client.get_submissions()
```

### Access to simulation data
```python
result = client.find_sim(sim_type="nbody")
# returns list of `Simulation` objects
```
The method `find_sim` accepts the following parameters for `nbody`
type:
- `integrator`: code or integrator used for gravitational integration
- `system`: type of modeled system (large-scale structure, galaxy cluster, galaxy, star cluster, planetary system) 
- `dynamics`: collisional or collisionless
- `symmetry`: assumed symmetry (none, central, axial, triaxial, planar). Default is `None`.
- `object`: relation to a concrete real object (e.g., Milky Way, Solar System,..). Default is `None`.
- `stevol`: involvement of stellar evolution (name of the model). Default is `None`.
- `gas`: involvement of gas dynamics (SPH, phenomenological model, ...). Default is `None`.
- `binaries`: involvement of binary systems (name of the model/method). Default is `False`.
- `releff`: involvement of relativistic effects (post-Newton, General Relativity). Default is `None`.


## Dependency
- `pyzmq` - ZeroMQ bindings for Python
