#remove old files
if [ -d work ]; then 
  rm -r work
fi

#create work directory
cp -r data work
cd work

#set the number of threads
export OMP_NUM_THREADS=1

#launch QE
qemdi.x -mdi "-role ENGINE -name QM -method TCP -port 8021 -hostname localhost" -in qe.in > qe.out &

#launch LAMMPS
lmp_mpi -mdi "-role ENGINE -name MM -method TCP -port 8021 -hostname localhost" -in lammps.in > lammps.out &

#launch driver
MDI_AIMD_Driver -mdi "-role DRIVER -name driver -method TCP -port 8021" &

wait
