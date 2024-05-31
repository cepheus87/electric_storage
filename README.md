# Electric storage simulator

Simulator of electric storage for eLicznki data

### Assumptions
- Storage starts with minimal available capacity (storage parameter)
- Charging and using energy processes are independent

### Flow
 
- Energy is used firstly from energy storage
- Energy storage is charged from produced energy
- Produced and used energy are balanced 
  - As a balanced energy only one type (used or produced) energy is returned in given time interval (one hour) 