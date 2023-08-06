from licant.core import core
import licant.make
import os


class toolchain:
	def __init__(self, cxx, cc, ld, ar, objdump, moc=None):
		self.cc = cc
		self.cxx = cxx
		self.ld = ld
		self.ar = ar
		self.objdump = objdump
		self.moc = moc

	def __repr__(self):
		return str(self.__dict__)


host_toolchain = toolchain(
	cxx="c++", 
	cc="cc", 
	ld="ld", 
	ar="ar", 
	objdump="objdump", 
	moc="moc"  # Qt support
)


def toolchain_gcc(prefix):
	if prefix is None:
		return host_toolchain

	return toolchain(
		cc=prefix+"gcc",
		cxx=prefix+"g++",
		ld=prefix+"ld",
		ar=prefix+"ar",
		objdump=prefix+"objdump",
		moc="moc")

def clang_toolchain():
	return toolchain(
		cc="clang++",
		cxx="clang",
		ld="ld",
		ar="ar",
		objdump="objdump",
		moc="moc")



class options:
	def __init__(
		self,
		toolchain=host_toolchain,
		include_paths=None,
		defines=None,
		cxx_flags="",
		cc_flags="",
		ld_flags="",
		ld_srcs_add="",
		ldscripts=None,
	):
		self.toolchain = toolchain
		self.incopt = licant.util.flag_prefix("-I", include_paths)
		self.defopt = licant.util.flag_prefix("-D", defines)
		self.ldscripts = licant.util.flag_prefix("-T", ldscripts)
		self.cxx_flags = cxx_flags
		self.cc_flags = cc_flags
		self.ld_flags = ld_flags
		self.ld_srcs_add = ld_srcs_add
		self.execrule = "{opts.toolchain.cxx} {opts.ld_flags} -Wl,--start-group {srcs} {opts.ld_srcs_add} -Wl,--end-group -o {tgt} {opts.ldscripts}"
		self.dynlibrule = "{opts.toolchain.cxx} --shared {opts.ld_flags} -Wl,--start-group {srcs} {opts.ld_srcs_add} -Wl,--end-group -o {tgt} {opts.ldscripts}"
		self.statlibrule = "{opts.toolchain.ar} rcs {tgt} {srcs}"
		self.cxxobjrule = "{opts.toolchain.cxx} -c {src} -o {tgt} {opts.incopt} {opts.defopt} {opts.cxx_flags}"
		self.ccobjrule = "{opts.toolchain.cc} -c {src} -o {tgt} {opts.incopt} {opts.defopt} {opts.cc_flags}"
		self.cxxdeprule = "{opts.toolchain.cxx} -MM {src} > {tgt} {opts.incopt} {opts.defopt} {opts.cxx_flags}"
		self.ccdeprule = "{opts.toolchain.cc} -MM {src} > {tgt} {opts.incopt} {opts.defopt} {opts.cc_flags}"
		self.mocrule = "{opts.toolchain.moc} {src} > {tgt}"

	def __str__(self):
		return f"(toolchain:{self.toolchain}, incopt:{self.incopt}, defopt:{self.defopt}, cxx_flags:{self.cxx_flags}, cc_flags:{self.cc_flags}, ld_flags:{self.ld_flags}, ld_srcs_add:{self.ld_srcs_add}, ldscripts:{self.ldscripts})"


cxx_ext_list = ["cpp", "cxx"]
cc_ext_list = ["cc", "c"]
asm_ext_list = ["asm", "s", "S"]


def object(src, tgt, opts=options(), type=None, deps=None, message="OBJECT {tgt}"):
	if deps is None:
		deps = [src]

	if type is None:
		ext = os.path.basename(src).split(".")[-1]

		if ext in cxx_ext_list:
			type = "cxx"
		elif ext in cc_ext_list:
			type = "cc"
		elif ext in asm_ext_list:
			type = "asm"
		else:
			print("Unrecognized extention: {}".format(licant.util.red(ext)))
			exit(-1)
	if type == "cxx":
		build = licant.make.Executor(opts.cxxobjrule)
	elif type == "cc":
		build = licant.make.Executor(opts.ccobjrule)
	elif type == "asm":
		build = licant.make.Executor(opts.ccobjrule)
	else:
		print(licant.util.red("Unrecognized extention"))
		exit(-1)
	core.add(
		licant.make.FileTarget(
			opts=opts, tgt=tgt, src=src, deps=deps, build=build, message=message
		)
	)


def moc(src, tgt, opts=options(), type=None, deps=None, message="MOC {tgt}"):
	if deps is None:
		deps = [src]

	core.add(
		licant.make.FileTarget(
			opts=opts,
			tgt=tgt,
			src=src,
			deps=deps,
			build=licant.make.Executor(opts.mocrule),
			message=message,
		)
	)


def depend(
	src, tgt, opts=options(), type=None, deps=None, message="DEPENDS {tgt}", **kwargs
):
	if deps is None:
		deps = [src]

	if type is None:
		ext = os.path.basename(src).split(".")[-1]

		if ext in cxx_ext_list:
			type = "cxx"
		elif ext in cc_ext_list:
			type = "cc"
		elif ext in asm_ext_list:
			type = "asm"
		else:
			print("Unrecognized extention: {}".format(licant.util.red(ext)))
			exit(-1)
	if type == "cxx":
		build = licant.make.Executor(opts.cxxdeprule)
	elif type == "cc":
		build = licant.make.Executor(opts.ccdeprule)
	elif type == "asm":
		build = licant.make.Executor(opts.ccdeprule)
	else:
		print(licant.util.red("Unrecognized extention"))
		exit(-1)

	core.add(
		licant.make.FileTarget(
			opts=opts,
			tgt=tgt,
			src=src,
			deps=deps,
			build=build,
			message=message,
			**kwargs
		)
	)


def executable(tgt, srcs, opts=options(), message="EXECUTABLE {tgt}"):
	core.add(
		licant.make.FileTarget(
			opts=opts,
			tgt=tgt,
			build=licant.make.Executor(opts.execrule),
			srcs=" ".join(srcs),
			deps=srcs,
			message=message,
		)
	)


def dynamic_library(tgt, srcs, opts=options(), message="DYNLIB {tgt}"):
	core.add(
		licant.make.FileTarget(
			opts=opts,
			tgt=tgt,
			build=licant.make.Executor(opts.dynlibrule),
			srcs=" ".join(srcs),
			deps=srcs,
			message=message,
		)
	)

def static_library(tgt, srcs, opts=options(), message="STATLIB {tgt}"):
	core.add(
		licant.make.FileTarget(
			opts=opts,
			tgt=tgt,
			build=licant.make.Executor(opts.statlibrule),
			srcs=" ".join(srcs),
			deps=srcs,
			message=message,
		)
	)

def make_gcc_binutils(pref):
	return toolchain(
		cxx=pref + "-g++",
		cc=pref + "-gcc",
		ld=pref + "-ld",
		ar=pref + "-ar",
		objdump=pref + "-objdump",
	)


def disassembler(target, *args):
	if len(args) <= 1:
		print("usage: disasm object_path asmlist_path")

	_target = core.get(args[0])
	_target.makefile()

	cmd = "{} -D {} > {}".format(_target.opts.binutils.objdump, _target.tgt, args[1])
	print(cmd)
	os.system(cmd)


binutils_target = licant.core.Target(
	tgt="binutils", deps=[], disasm=disassembler, actions={"disasm"}
)

core.add(binutils_target)
