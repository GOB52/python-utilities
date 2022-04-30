# python-utilities
[日本語/Japanese](README.ja.md)  
Utility scripts by Pyhton3  

## raise_version.py

### Overview
Raise version by [semantic versioning](https://semver.org/) for Arduino Library.  
Raise version and update **library.properties** and **library.json** if exists.  
Output version definition C style header file if you want.  

### Usage

Execute on the directory where library.properties or library.json are located.  
```
python3 raise_version.py [-h] [--execute] [--raising {MAJOR,MINOR,PATCH}] [--source SOURCE] [--prefix PREFIX] [--info] [--verbose]
```

|option|description|
----|---- 
| --execute, -e | Do raising. **Dry-run if not set** |
| --raising {MAJOR,MINOR,PATCH}, -r {MAJOR,MINOR,PATCH} |  Increment target (PATCH as default) |
| --source SOURCE, -s SOURCE |  Output source file path |
| --prefix PREFIX, -p PREFIX |  Definition prefix for source (require if --source) |
|  --info, -i | Show version from property and json if exists|


### e.g.
If library.properties and library.json has version 2.3.4  
```
python3 raise_version.py --execute --raising MINOR --source lib_version.hpp --prefix YOUR_LIBRARY_PREFIX
```

Raise from **2.3.4** to **2.4.0**  
Update library.properties and library.json  

library.properties  
```
version=2.4.0
```

library.json  
```
  "version": "2.4.0",
```

Output C style header  
lib\_version.hpp  
```C
#ifndef YOUR_LIBRARY_PREFIX_VERSION_HPP
#define YOUR_LIBRARY_PREFIX_VERSION_HPP

#define YOUR_LIBRARY_PREFIX_VERSION_MAJOR 2
#define YOUR_LIBRARY_PREFIX_VERSION_MINOR 4
#define YOUR_LIBRARY_PREFIX_VERSION_PATCH 0

#define YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY_AGAIN(x) #x
#define YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY(x) YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY_AGAIN(x)

#define YOUR_LIBRARY_PREFIX_VERSION_VALUE ((YOUR_LIBRARY_PREFIX_VERSION_MAJOR << 16) | (YOUR_LIBRARY_PREFIX_VERSION_MINOR << 8) | (YOUR_LIBRARY_PREFIX_VERSION_PATCH))
#define YOUR_LIBRARY_PREFIX_VERSION_STRING YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY(YOUR_LIBRARY_PREFIX_VERSION_MAJOR.YOUR_LIBRARY_PREFIX_VERSION_MINOR.YOUR_LIBRARY_PREFIX_VERSION_PATCH)

#endif
```
