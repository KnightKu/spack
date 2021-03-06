# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack import *


class Cloverleaf(MakefilePackage):
    """Proxy Application. CloverLeaf is a miniapp that solves the
       compressible Euler equations on a Cartesian grid,
       using an explicit, second-order accurate method.
    """

    homepage = "http://uk-mac.github.io/CloverLeaf"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/CloverLeaf/CloverLeaf-1.1.tar.gz"

    tags = ['proxy-app']

    version('1.1', '65652b30a64eb237ec844a6fdd4cd518')

    variant('build', default='ref', description='Type of Parallelism Build',
            values=('cuda', 'mpi_only', 'openacc_cray',
                    'openmp_only', 'ref', 'serial'))

    depends_on('mpi', when='build=cuda')
    depends_on('mpi', when='build=mpi_only')
    depends_on('mpi', when='build=openacc_cray')
    depends_on('mpi', when='build=ref')
    depends_on('cuda', when='build=cuda')

    @property
    def type_of_build(self):
        build = 'ref'

        if 'build=cuda' in self.spec:
            build = 'CUDA'
        elif 'build=mpi_only' in self.spec:
            build = 'MPI'
        elif 'build=openacc_cray' in self.spec:
            build = 'OpenACC_CRAY'
        elif 'build=openmp_only' in self.spec:
            build = 'OpenMP'
        elif 'build=serial' in self.spec:
            build = 'Serial'

        return build

    @property
    def build_targets(self):
        targets = ['--directory=CloverLeaf_{0}'.format(self.type_of_build)]

        if 'mpi' in self.spec:
            targets.append('MPI_COMPILER={0}'.format(self.spec['mpi'].mpifc))
            targets.append('C_MPI_COMPILER={0}'.format(self.spec['mpi'].mpicc))
        else:
            targets.append('MPI_COMPILER=f90')
            targets.append('C_MPI_COMPILER=cc')

        if '%gcc' in self.spec:
            targets.append('COMPILER=GNU')
        elif '%cce' in self.spec:
            targets.append('COMPILER=CRAY')
        elif '%intel' in self.spec:
            targets.append('COMPILER=INTEL')
        elif '%pgi' in self.spec:
            targets.append('COMPILER=PGI')
        elif '%xl' in self.spec:
            targets.append('COMPILER=XLF')

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install('README.md', prefix.doc)
        install('documentation.txt', prefix.doc)

        install('CloverLeaf_{0}/clover_leaf'.format(self.type_of_build),
                prefix.bin)
        install('CloverLeaf_{0}/clover.in'.format(self.type_of_build),
                prefix.bin)

        for f in glob.glob(
                'CloverLeaf_{0}/*.in'.format(self.type_of_build)):
            install(f, prefix.doc.tests)
