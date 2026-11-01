set(libsiesta_sources

  Fstack.T90
  Pair.T90
  alloc.F90
  alloc_handlers_m.F90
  amn.F90
  arw.f
  atm_types.f
  atmfuncs.f
  atmparams.f
  atom.F
  atom_graph.F90
  atom_options.F90
  atomlist.f
  atomlwf.F
  automatic_cell.f
  bands.F
  basic_func.inc
  basic_type.inc
  basis_enthalpy.f90
  basis_io.F
  basis_specs.f
  basis_types.f
  bessph.f
  bloch_unfold.F90
  bonds.f
  born_charge.F
  broadcast_basis.F
  broadcast_fdf_struct.F90
  broadcast_projections.F
  broyden_optim.F
  bsc_cellxc.F
  byte_count.F90
  cart2frac.f
  cell_broyden_optim.F
  cell_fire_optim.F
  cellsubs.f
  cgvc.F
  cgvc_zmatrix.F
  cgwf.F
  chemical.f
  chempot.F
  chkdim.f
  chkgmx.f
  class_Data1D.F90
  class_Data1D.T90
  class_Data2D.F90
  class_Data2D.T90
  class_Data3D.F90
  class_Data3D.T90
  class_Distribution.F90
  class_Fstack_Data1D.F90
  class_Fstack_Pair_Data1D.F90
  class_Fstack_Pair_Geometry_SpData2D.F90
  class_Fstack_Pair_SpData1D.F90
  class_Geometry.F90
  class_OrbitalDistribution.F90
  class_Pair_Data1D.F90
  class_Pair_Geometry_SpData2D.F90
  class_Pair_SpData1D.F90
  class_SpData1D.F90
  class_SpData1D.T90
  class_SpData2D.F90
  class_SpData2D.T90
  class_SpData3D.F90
  class_SpData3D.T90
  class_Sparsity.F90
  class_TriMat.F90
  class_TriMat.T90
  cli_m.f90
  coceri.f
  compute_dm.F
  compute_ebs_shift.F90
  compute_energies.F90
  compute_max_diff.F90
  compute_norm.F
  compute_pw_matrix.F90
  ${PROJECT_BINARY_DIR}/Src/configured_values_m.F90
  conjgr.f
  conjgr_old.f
  constr.f
  coor.F
  coxmol.f
  cranknic_evolg.F90
  cranknic_evolk.F90
  create_Sparsity_SC.F90
  create_Sparsity_Union.F90
  cross.f
  debugmpi.F
  delk.F90
  denmat.F
  denmatlomem.F
  densematrix.f90
  detover.F
  dfscf.f
  dftu.F
  dftu_specs.f
  dhscf.F
  dhsdr_m.F90
  diag.F90
  diag2g.F
  diag2k.F
  diag2kp.F90
  diag2kspiral.F90
  diag3g.F
  diag3k.F
  diag3kp.F90
  diag_option.F90
  diagg.F
  diagk.F
  diagk_file.F
  diagkp.F
  diagkp_velocity.F90
  diag2kp_velocity.F90
  diag3kp_velocity.F90
  diagmemory.F
  diagon.F
  diagonalizeHk.F90
  diagpol.f
  digcel.f
  dipole.F90
  dismin.f
  dm_charge.F90
  dnaefs.F
  domain_decom.F
  doping_uniform.F
  dot.f
  dynamics.F
  egandd.F
  eggbox.F
  electrostatic.f
  ener3.F
  ener3lomem.F
  errorf.f
  extrae_eventllist.F90
  extrae_module.f90
  extrapolateSpData2D.F90
  extrapolon.f
  fc_matrices_m.F90
  fdf_extra.F90
  fermid.F
  fft.F
  fft1d.F
  fftw3_wrapper.F90
  files.f
  final_H_f_stress.F
  find_kgrid.F
  fire_optim.F
  flook_siesta.F90
  fold_auxcell.f90
  forhar.F
  fsiesta_mpi.F90
  fsockets.f90
  geom_helper.f90
  get_kpoints_scale.f90
  globalise.F
  gradient.F
  gradientlomem.F
  grimme_dispersion_m.F90
  grdsam.F
  hamann.f90
  hsparse.F
  idiag.f
  init_output.f90
  initatom.f
  initparallel.F
  interpolation.f90
  intrinsic_missing.F90
  inver.f
  io.f
  io_ext.f90
  io_sparse.F90
  iocg.f
  iodm.F
  iodm_netcdf.F90
  iodmhs_netcdf.F90
  ioeig.f
  iofa.f90
  iogrid_netcdf.F90
  iokp.f
  iolwf.F
  iomd.f
  iopipes.F90
  iosockets.F90
  iotdxv.F
  iowfs_netcdf.F90
  ioxv.F
  iozm.F
  ipack.f
  kgrid.F
  kgridinit.F
  kinefsm.F
  kpoint_convert.f90
  kpoint_dos.F90
  kpoint_ldos.F90
  kpoint_pdos.F90
  kpoint_scf.F90
  kpoint_t.F90
  ksv.f
  ksvinit.F
  linpack.F
  listsc.f
  local_DOS.F90
  m_broyddj.f90
  m_broyddj_nocomm.f90
  m_broyden_mixing.f
  m_cell.f
  m_char.f90
  m_charge_add.F90
  m_check_walltime.f90
  m_chempotwann.F90
  m_chess.F90
  m_cite.F90
  m_convergence.f90
  m_dftu_so.F90
  m_digest_nnkp.F90
  m_diis.F90
  m_dipol.F90
  m_dminim.F90
  m_dscfcomm.F
  m_efield.F90
  m_elsi_interface.F90
  m_energies.F90
  m_eo.F90
  m_evolve.F90
  m_exp_coord.F90
  m_fft_gpfa.F
  m_filter.f90
  m_fire.f90
  m_fire_mixing.f
  m_fire_para.F90
  m_fixed.F90
  m_forces.F90
  m_gauss_fermi_17.f90
  m_gauss_fermi_18.f90
  m_gauss_fermi_19.f90
  m_gauss_fermi_20.f90
  m_gauss_fermi_22.f90
  m_gauss_fermi_24.f90
  m_gauss_fermi_26.f90
  m_gauss_fermi_28.f90
  m_gauss_fermi_30.f90
  m_gauss_fermi_inf.f90
  m_gauss_quad.f90
  m_geom_aux.f90
  m_geom_box.f90
  m_geom_coord.f90
  m_geom_objects.f90
  m_geom_plane.f90
  m_geom_square.f90
  m_getopts.f90
  m_handle_sparse.F90
  m_hartree_add.F90
  io_hsx.F90
  m_initwf.F90
  m_integrate.f90
  m_interpolate.F90
  m_inversemm.F90
  m_io.f
  m_io_yaml.F90
  m_iodipol.F90
  m_iodm.F90
  m_iodm_old.F
  m_iorho.F
  m_iostruct.f
  m_iotddft.F90
  m_iterator.f90
  m_kinetic.F90
  m_mat_invert.F90
  m_matdiag.F90
  m_matio.F90
  m_matswinvers.F90
  m_mesh_node.F90
  m_mixing.F90
  m_mixing_scf.F90
  m_monitor.F90
  m_mpi_utils.F
  m_ncdf_siesta.F90
  m_new_dm.F90
  m_noccbands.f
  m_ntm.F90
  m_occ_proj_dftu.F90
  m_options.f90
  m_orderbands.F
  m_os.F90
  m_overkkneig.F90
  partial_charges.F90
  m_pivot.F90
  m_pivot_array.f90
  m_pivot_methods.F90
  m_planewavematrix.F90
  m_planewavematrixvar.F90
  m_pot_dftu.F90
  m_redist_spmatrix.F90
  m_region.F90
  m_rhog.F90
  m_rmaxh.F90
  m_sparse.F90
  m_sparsity_handling.F90
  m_spin.F90
  m_steps.F90
  m_stress.F90
  m_supercell.F90
  m_svd.F90
  m_switch_local_proj.F90
  m_target_stress.F90
  m_test_io.F90
  m_timer.F90
  m_transiesta.F90
  m_trialorbitalclass.f90
  m_wigner_d.f90
  m_trimat_invert.F90
  m_ts_aux.F90
  m_ts_cctype.f90
  m_ts_chem_pot.F90
  m_ts_contour.f90
  m_ts_contour_eq.f90
  m_ts_contour_neq.f90
  m_ts_debug.F90
  m_ts_dm_update.F90
  m_ts_elec_se.F90
  m_ts_electrode.F90
  m_ts_full_scat.F90
  m_ts_fullg.F90
  m_ts_fullk.F90
  m_ts_gf.F90
  m_ts_global_vars.f90
  m_ts_hartree.F90
  ts_io_hs.F90
  m_ts_io_contour.f90
  m_ts_io_ctype.f90
  m_ts_iodm.F90
  m_ts_method.f90
  m_ts_mumps_init.F90
  m_ts_mumps_scat.F90
  m_ts_mumpsg.F90
  m_ts_mumpsk.F90
  m_ts_options.F90
  m_ts_pivot.F90
  m_ts_rgn2trimat.F90
  m_ts_sparse.F90
  m_ts_sparse_helper.F90
  m_ts_tdir.f90
  m_ts_tri_common.F90
  m_ts_tri_init.F90
  m_ts_tri_scat.F90
  m_ts_trig.F90
  m_ts_trik.F90
  m_ts_trimat_invert.F90
  m_ts_voltage.F90
  m_ts_weight.F90
  m_uuid.f90
  m_vee_integrals.F90
  m_wallclock.f90
  m_walltime.f90
  m_wannier_in_nao.F90
  m_w90_wrapper.F90
  m_writedelk.F
  m_zminim.F90
  madelung.f
  matel.F90 matel_params.f90 matel_registry.F90 matel_table.F90 matel_ylm.F90
  md_out.F90
  memory.F
  memory_all.F90
  memory_log.F90
  memory_snapshot.f90
  mesh.F
  meshcomm.F
  meshdscf.F
  meshphi.F
  meshsubs.F
  metaforce.F
  minvec.f
  mixer.F
  mmio.F
  mmn.F90
  mneighb.f
  molecularmechanics.F90
  moments.F
  moreParallelSubs.F90
  moremeshsubs.F
  mulliken.F
  naefs.F
  nag.f
  ncdf_io.F90
  nlefsm.f
  normalize_dm.F90
  obc.f
  object_debug.F90
  ofc.f90
  on_subs.F
  onmod.F
  optical.F
  ordern.F
  outcell.f
  outcoor.f
  overfsm.f90
  overlap.f
  parallel.F
  parallelsubs.F
  parsing.f
  pdos.F90
  pdos2g.F90
  pdos2k.F90
  pdos2kp.F90
  pdos3g.F90
  pdos3k.F90
  pdos3kp.F90
  pdosg.F90
  pdosk.F90
  pdoskp.F90
  periodic_table.f
  phirphi.f
  phirphi_opt.f
  pixmol.f
  plcharge.F
  poison.F
  posix_calls.f90
  post_scf_work.F
  precision.F
  print_spin.F90
  printmatrix.F
  projected_DOS.F90
  propor.f
  proximity_check.F
  pspltm1.F
  pxf.F90
  qmmm/qmmm_core.f90
  qmmm/qmmm_ewald.f90
  qmmm/qmmm_helpers.f90
  qmmm/qmmm_interface.F90
  qmmm/qmmm_mmforces.F90
  qmmm/qmmm_mneighb.f90
  qmmm/qmmm_pcpot.F90
  qmmm/qmmm_structure.f90
  qsort.F
  radfft.f
  radial.f
  randomg.f90
  read_options.F90
  read_xc_info.F
  reclat.f
  redcel.F
  register_rfs.F90
  reinit_m.F90
  remove_intramol_pressure.f90
  reoptical.F
  reord.f
  reordpsi.F
  restructSpData2D.F90
  rhofft.F
  rhooda.F
  rhoofd.F90
  rhoofdsp.F90
  runinfo_m.F90
  rusage.f90
  sankey_change_basis.F90
  save_density_matrix.F90
  savepsi.F
  scfconvergence_test.F
  schecomm.F
  setatomnodes.F
  setspatial.f
  setup_H0.F
  setup_hamiltonian.F
  setup_ordern_indexes.F90
  shaper.f
  show_distribution.f
  siesta2wannier90.F90
  siesta_analysis.F90
  siesta_cml.f90
  siesta_cmlsubs.F90
  siesta_dicts.F90
  siesta_end.F
  siesta_forces.F90
  siesta_geom.F90
  siesta_handlers_m.F90
  siesta_init.F
  siesta_master.f90
  siesta_move.F
  siesta_options.F90
  option_charges.f90
  siesta_tddft.F90
  siesta_version_info.F90
  sockets.c
  sorting.f
  sparse_matrices.F90
  spatial.F
  spher_harm.f
  spin_subs.F90
  spinorbit.f
  state_analysis.F
  state_init.F
  struct_init.F
  timer.F90
  timer_tree.f90
  timestamp.f90
  transition_rate.F
  ts_charge.F90
  ts_dq.F90
  ts_energies.F90
  ts_electrode.F90
  ts_init.F90
  ts_kpoint_scf.F90
  ts_show_regions.f90
  typecell.f
  uncell.f
  vacuum_level.f90
  velocity_shift.F90
  vmat.F90
  vmatsp.F90
  vmb.F
  volcel.f
  wannier90_types.f
  w90_wrapper_types.f
  wavefunctions.F90
  write_inp_wannier.F90
  write_md_record.F
  write_orb_indx.f90
  write_raw_efs.f90
  write_subs.F
  writewave.F
  xml.f
  zm_broyden_optim.F
  zm_fire_optim.F
  zmatrix.F
)

if( SIESTA_WITH_PROFILE_NVTX )
  list(APPEND libsiesta_sources nvtx-profiling/nvtx_wrapper.F90)
  set_source_files_properties(
             timer.F90
             nvtx-profiling/nvtx_wrapper.F90
             PROPERTIES  COMPILE_DEFINITIONS "__PROFILE_NVTX")
  if ("${SIESTA_PROFILE_NVTX_LIBRARY}" STREQUAL "")
     message(WARNING "SIESTA_PROFILE_NVTX_LIBRARY is not defined. Will not profile")
     list(APPEND libsiesta_sources nvtx-profiling/dummy_nvtx.c)
  endif()

endif()

if( SIESTA_WITH_PEXSI )
  list(APPEND libsiesta_sources

    pexsi-solver/m_pexsi.F90
    pexsi-solver/m_pexsi_dos.F90
    pexsi-solver/m_pexsi_driver.F90
    pexsi-solver/m_pexsi_local_dos.F90
    pexsi-solver/siesta_pexsi_interface.F90
 )
endif()

# Create libsiesta target.
siesta_add_library(${PROJECT_NAME}.libsiesta
    ${libsiesta_sources}
  EXPORT_NAME libsiesta
  OUTPUT_NAME siesta
  CUSTOM_TARGET libsiesta
  NAMESPACE_TARGET libsiesta)

target_compile_definitions(${PROJECT_NAME}.libsiesta
  PUBLIC
  $<$<BOOL:${SIESTA_WITH_MPI}>:MPI>
  $<$<BOOL:${SIESTA_WITH_GRID_SP}>:GRID_SP>
  $<$<BOOL:${SIESTA_WITH_ELPA}>:SIESTA__ELPA>
  $<$<BOOL:${SIESTA_WITH_PEXSI}>:SIESTA__PEXSI>
  $<$<BOOL:${SIESTA_WITH_CHESS}>:SIESTA__CHESS>
  $<$<BOOL:${SIESTA_WITH_ELSI}>:SIESTA__ELSI>
  $<$<BOOL:${ELSI_HAS_PEXSI}>:ELSI_HAS_PEXSI>
  $<$<BOOL:${ELSI_HAS_MAGMA}>:ELSI_HAS_MAGMA>
  $<$<BOOL:${ELSI_HAS_EIGENEXA}>:ELSI_HAS_EIGENEXA>
  $<$<BOOL:${ELSI_HAS_SIPS}>:ELSI_HAS_SIPS>
  $<$<BOOL:${ELSI_HAS_EXTERNAL_ELPA}>:ELSI_HAS_EXTERNAL_ELPA>
  $<$<NOT:$<BOOL:${ELSI_HAS_EXTERNAL_ELPA}>>:ELPA_API_VERSION=20200000>
  $<$<BOOL:${SIESTA_WITH_NETCDF}>:CDF>
  $<$<BOOL:${SIESTA_WITH_NCDF}>:NCDF NCDF_4>
  $<$<BOOL:${SIESTA_WITH_NCDF_PARALLEL}>:NCDF_PARALLEL>
  $<$<BOOL:${SIESTA_WITH_FFTW}>:SIESTA__FFTW ${SIESTA_FFTW_PRECISION}>
  $<$<BOOL:${SIESTA_WITH_FLOOK}>:SIESTA__FLOOK>
  $<$<BOOL:${SIESTA_WITH_DFTD3}>:SIESTA__DFTD3>
  $<$<BOOL:${SIESTA_WITH_WANNIER90}>:SIESTA__WANNIER90>
)

# CMake linking order I do not understand
# The xmlf90 order seems important, but it shouldn't be since
# cmake should be able to determine correct dependency order.
# 1. xmlf90 before libpsml does not work
# 2. xmlf90 after libpsml works
# 3. removing xmlf90 works, since libpsml depends on xmlf90 (see top-level CMakeLists.txt)
# Huh..?
#
# A similar issue arises when the NetCDF installation is compiled with MPI capability. The
# order of the mpi_siesta (or MPI::MPI_Fortran in general) and the NetCDF targets is significant.
# For example, in CINECA with intel-oneapi-mpi and the GNU compiler, if NetCDF comes first the
# intel-specific 'include' directory is put first in the '-I' list by CMake, instead of the
# 'include/gfortran/<version-number>' directory. Putting the MPI dependency first seems to fix
# the issue.
#
if(SIESTA_WITH_ELPA AND (NOT SIESTA_HAS_ELPA_THROUGH_ELSI))
  set(SIESTA_NEEDS_ELPA_TARGET TRUE)
else()
  set(SIESTA_NEEDS_ELPA_TARGET FALSE)
endif()
message(STATUS "SIESTA_NEEDS_ELPA_TARGET: ${SIESTA_NEEDS_ELPA_TARGET}")

target_link_libraries(${PROJECT_NAME}.libsiesta
  PUBLIC
  $<$<BOOL:${SIESTA_WITH_MPI}>:${PROJECT_NAME}.mpi>
  $<$<BOOL:${SIESTA_WITH_NCDF}>:${PROJECT_NAME}.libncdf>
  $<$<BOOL:${SIESTA_WITH_NETCDF}>:NetCDF::NetCDF_Fortran>
  # Internal projects
  ${PROJECT_NAME}.libsys
  ${PROJECT_NAME}.libncps
  ${PROJECT_NAME}.libpsop
  ${PROJECT_NAME}.libms
  ${PROJECT_NAME}.libunits
  ${PROJECT_NAME}.mpi_macros  # adding mpi_macros include path
  libfdf::libfdf
  libpsml::libpsml
  libgridxc::libgridxc
  # Optional dependencies
  $<$<BOOL:${SIESTA_WITH_FLOOK}>:flook::flook>
  $<$<BOOL:${SIESTA_WITH_WANNIER90}>:wrapper-wannier90::wrapper-wannier90>
  $<$<OR:$<BOOL:${SIESTA_WITH_NCDF}>,$<BOOL:${SIESTA_WITH_FLOOK}>>:${PROJECT_NAME}.libfdict>
  $<$<BOOL:${SIESTA_WITH_DFTD3}>:s-dftd3::s-dftd3>
  $<$<BOOL:${SIESTA_WITH_FFTW}>:${SIESTA_FFTW_TARGET}>
  $<$<BOOL:${SIESTA_NEEDS_ELPA_TARGET}>:Elpa::elpa>
  $<$<BOOL:${SIESTA_WITH_PEXSI}>:${PROJECT_NAME}::pexsi>
  $<$<BOOL:${SIESTA_WITH_CHESS}>:CheSS::CheSS>
  $<$<BOOL:${SIESTA_WITH_ELSI}>:elsi::elsi>
  $<$<BOOL:${SIESTA_WITH_MPI}>:SCALAPACK::SCALAPACK>
  # Forced external dependencies
  LAPACK::LAPACK
  $<$<BOOL:${SIESTA_WITH_OPENMP}>:OpenMP::OpenMP_Fortran>
  # To link properly the C++ runtime
  $<$<BOOL:${ELSI_HAS_PEXSI}>:${PROJECT_NAME}.cxx_dummy_lib>
  # Profiling
  $<$<BOOL:${SIESTA_WITH_PROFILE_NVTX}>:${PROJECT_NAME}.nvtx-c>
)

## For stuff that depends on libsiesta, add its include directory
target_include_directories(${PROJECT_NAME}.libsiesta
  PUBLIC
    "${CMAKE_CURRENT_BINARY_DIR}"
  )


# Now create the actual siesta executable
siesta_add_executable(${PROJECT_NAME}.siesta
    siesta.F
  EXPORT_NAME siesta
  # Having an output-name also creates the *target* which can confuse
  # Ninja. Hence we don't create CUSTOM_TARGET in the siesta_add_executable
  # invocation.
  OUTPUT_NAME siesta
  NAMESPACE_TARGET siesta)

target_link_libraries(${PROJECT_NAME}.siesta
  PRIVATE
    ${PROJECT_NAME}.libsiesta
  )

# Add diagonalization options
# grep -e SIESTA__MRRR -e SIESTA__DIAG_2STAGE * | tr ':' ' ' | awk '{print $1}' | uniq
set_property(
  SOURCE
    diag.F90
    diag_option.F90
  APPEND PROPERTY COMPILE_DEFINITIONS
  $<$<BOOL:${HAS_MRRR}>:SIESTA__MRRR>
  $<$<BOOL:${LAPACK_HAS_2STAGE}>:SIESTA__DIAG_2STAGE>
  "$<$<BOOL:${SIESTA_WITH_WANNIER90}>:SIESTA__WANNIER90>"
  )

# Add 3m options
# grep USE_GEMM3M * | tr ':' ' ' | awk '{print $1}' | uniq
set_property(
  SOURCE
    m_io_yaml.F90
    m_mat_invert.F90
    m_trimat_invert.F90
    m_ts_electrode.F90
    m_ts_full_scat.F90
    m_ts_mumps_scat.F90
    m_ts_trimat_invert.F90
    m_ts_tri_scat.F90
    simple-version.F90
  APPEND PROPERTY COMPILE_DEFINITIONS
  $<$<BOOL:${BLAS_HAS_GEMM3M}>:USE_GEMM3M>
  )

set_property(
  SOURCE
    siesta_version_info.F90
  APPEND PROPERTY COMPILE_DEFINITIONS
  $<$<BOOL:${ELSI_HAS_EXTERNAL_ELPA}>:ELSI_HAS_EXTERNAL_ELPA>
  $<$<BOOL:${ELSI_HAS_PEXSI}>:ELSI_HAS_PEXSI>
  $<$<BOOL:${ELSI_HAS_CUDA}>:ELSI_HAS_CUDA>
  $<$<BOOL:${ELPA_HAS_GPU_SUPPORT}>:ELPA_HAS_GPU_SUPPORT>

  )


if( LIBPSML_USES_PROCEDURE_POINTER )
  # Deal correctly with libpsml support
  set_property(SOURCE
      siesta_handlers_m.F90
    APPEND PROPERTY COMPILE_DEFINITIONS
    SIESTA__PSML_HAS_PP
  )
endif()
if( LIBGRIDXC_USES_PROCEDURE_POINTER )
  # Deal correctly with libgridxc support
  set_property(SOURCE
      siesta_handlers_m.F90
    APPEND PROPERTY COMPILE_DEFINITIONS
    SIESTA__GRIDXC_HAS_PP
  )
endif()


#
#  Compile some files with no optimization for the Intel compiler
#
if( CMAKE_Fortran_COMPILER_ID MATCHES Intel )

  set(DEBUG_OPTIONS_LIST "${Fortran_FLAGS_DEBUG}")  # Should set this
  separate_arguments(DEBUG_OPTIONS_LIST)   # Turns empty space to ';'
  message(STATUS "Debug flags for some files in Src: ${DEBUG_OPTIONS_LIST}")
  set_source_files_properties(
    atom.F
	  state_analysis.F
	  create_Sparsity_SC.F90
    PROPERTIES
    COMPILE_OPTIONS "${DEBUG_OPTIONS_LIST}"
  )
endif()

if( CMAKE_Fortran_COMPILER_ID MATCHES NVHPC )

  set_property(
    SOURCE
    m_ts_electrode.F90
    APPEND PROPERTY COMPILE_OPTIONS
    "-Mnoinline"
  )
endif()

# Create string with line breaks and continuations in order to not exceed
# the maximum line length (132 characters) of Fortran 2003.
# There is not check that the maximum number of continuation lines
# (255 in Fortran 2003) is not exceeded.
siesta_conda_fix(Fortran_FLAGS_CURRENT)
siesta_get_multiline(LENGTH 128
  Fortran_FLAGS_CURRENT
  OUTPUT Fortran_FLAGS_CURRENT_multiline
  )

# This isn't used since it may contain generator
# expressions, and the multiline method can cut it
# at bad positions.
get_target_property(
  Fortran_PPFLAGS_CURRENT
  ${PROJECT_NAME}.libsiesta
  COMPILE_DEFINITIONS
  )

siesta_conda_fix(Fortran_PPFLAGS_CURRENT)
siesta_get_multiline(LENGTH 128
  Fortran_PPFLAGS_CURRENT
  OUTPUT Fortran_PPFLAGS_CURRENT_multiline
  )

# Create version file with the version string implemented
# TODO this will only be generated at cmake generation, i.e.
#  git pull | cmake --build_build -- siesta-siesta
# will not regenerate the version information.
configure_file(
  version-info-template.inc
  version-info.inc
  @ONLY
  )

# Configure file with defaults determined at build configuration time
# (e.g. SIESTA_ELPA_GPU_STRING)
configure_file(
  configured_values_m.F90.in
  "${PROJECT_BINARY_DIR}/Src/configured_values_m.F90"
  @ONLY
  )

if( SIESTA_INSTALL )
  install(
    TARGETS ${PROJECT_NAME}.libsiesta
    RUNTIME DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    )
  install(
    TARGETS ${PROJECT_NAME}.siesta
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
    )
endif()

