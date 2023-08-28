import mdi

# Initialize the MDI Library
options = "-role DRIVER -name aimd -method TCP -port 8021"
mdi.MDI_Init(options)

# Connect to the engines
engines = { 'QM': None, 'MM': None }
for iengine in range( len(engines) ):
    comm = mdi.MDI_Accept_communicator()

    # Get the name of this engine
    mdi.MDI_Send_command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH,
                        mdi.MDI_CHAR, comm)
    print("Connected to engine: " + str(name), flush=True)
    engines[name] = comm

# Get the number of atoms in the simulation
mdi.MDI_Send_command("<NATOMS", engines['MM'])
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, engines['MM'])

# Have the MM engine initialize a new MD simulation
mdi.MDI_Send_command("@INIT_MD", engines['MM'])

# Perform each iteration of the AIMD simulation
for iteration in range(10):

    # Have the MM engine proceed to the next @FORCES node
    mdi.MDI_Send_command("@FORCES", engines['MM'])

    # Receive the coordinates from the MM engine
    mdi.MDI_Send_command("<COORDS", engines['MM'])
    coords = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, engines['MM'])

    # Send the coordinates to the QM engine
    mdi.MDI_Send_command(">COORDS", engines['QM'])
    mdi.MDI_Send(coords, 3*natoms, mdi.MDI_DOUBLE, engines['QM'])

    # Receive the forces from the QM engine
    mdi.MDI_Send_command("<FORCES", engines['QM'])
    forces = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, engines['QM'])

    # Send the forces to the MM engine
    mdi.MDI_Send_command(">FORCES", engines['MM'])
    mdi.MDI_Send(forces, 3*natoms, mdi.MDI_DOUBLE, engines['MM'])

    # Receive the energy from the QM engine
    mdi.MDI_Send_command("<ENERGY", engines['QM'])
    qm_energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, engines['QM'])

    # Receive the energy from the MM engine
    mdi.MDI_Send_command("<ENERGY", engines['MM'])
    mm_energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, engines['MM'])

    print(str(mm_energy) + " " + str(qm_energy), flush=True)

# Send the "EXIT" command to each of the engines
for engine in engines.values():
    mdi.MDI_Send_command("EXIT", engine)

