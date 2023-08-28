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
/repo/build/q-e/MDI/src/qemdi.x -mdi "-role ENGINE -name QM -method TCP -port 8021 -hostname localhost" -in qe.in > qe.out &

#launch LAMMPS
/repo/build/lammps/build/lmp_mpi -mdi "-role ENGINE -name MM -method TCP -port 8021 -hostname localhost" -in lammps.in > lammps.out &

#launch driver
python /repo/tests/python/aimd_driver.py &

wait
