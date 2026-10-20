"""Referee L011 round 2: make nauty.h / gtools.h / naututil.h from the *-h.in templates by @var@ substitution
(own script; the tarball's configure is not run).  x86-64 Linux, gcc.  Usage: python3 -I hdrs.py SRC DST"""
import os, re, sys
src, dst = sys.argv[1], sys.argv[2]
yes = """header_unistd_h header_sys_types_h header_stddef_h header_stdlib_h header_string_h header_limits_h header_stdint_h
header_errno_h header_sys_wait_h header_signal_h malloc_dec has_math_inf have_flockfile stdio_nolock have_ansicontrols
flex_array_ok have_clz have_clzl have_clzll have_popcnt have_popcntl have_popcntll have_perror have_pipe have_wait have_popen
popen_dec ftell_dec fdopen_dec sort_newparams_ok sort_size_ok have_pid_t putenv_dec setenv_dec have_putenv have_setenv have_fork
have_fseeko have_sigaction have_sigprocmask have_isatty have_times have_time have_getrusage have_gettimeofday
have_clock_gettime have_clock""".split()
no = "default_wordsize have_hwlzcnt have_hwpopcnt have_mmpop32 have_mmpop64 is_ARM64 allow_interrupt tls_supported have_gunzip".split()
V = dict((k, '1') for k in yes); V.update((k, '0') for k in no)
V.update(PACKAGE_VERSION='2.8.8', configure_input='hdrs.py (referee L011 r2)', edit_msg='generated, do not edit',
         use_tls='', ac_cv_tls='', ac_cv_noret='__attribute__((__noreturn__))', ac_cv_sys_file_offset_bits='64',
         ac_cv_sizeof_int='4', ac_cv_sizeof_long='8', ac_cv_sizeof_unsigned___int128='16', ac_cv_sizeof___uint128_t='16',
         ac_cv_sizeof_voidp='8', sort_prog='sort')
os.makedirs(dst, exist_ok=True)
for nm in ('nauty', 'gtools', 'naututil'):
    t = open(os.path.join(src, nm + '-h.in')).read()
    left = set(re.findall(r'@(\w+)@', t)) - set(V)
    assert not left, (nm, left)
    open(os.path.join(dst, nm + '.h'), 'w').write(re.sub(r'@(\w+)@', lambda mo: V[mo.group(1)], t))
print('ok', dst)
