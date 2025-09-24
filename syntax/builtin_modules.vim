if !has('vim9script')
	finish
endif

vim9script

const builtin_modules =
	[
		'add_host',
		'apt',
		'apt_key',
		'apt_repository',
		'assemble',
		'assert',
		'async_status',
		'blockinfile',
		'command',
		'copy',
		'cron',
		'deb822_repository',
		'debconf',
		'debug',
		'dnf',
		'dnf5',
		'dpkg_selections',
		'expect',
		'fail',
		'fetch',
		'file',
		'find',
		'gather_facts',
		'get_url',
		'getent',
		'git',
		'group',
		'group_by',
		'hostname',
		'import_playbook',
		'import_role',
		'import_tasks',
		'include_role',
		'include_tasks',
		'include_vars',
		'iptables',
		'known_hosts',
		'lineinfile',
		'meta',
		'mount_facts',
		'package',
		'package_facts',
		'pause',
		'ping',
		'pip',
		'raw',
		'reboot',
		'replace',
		'rpm_key',
		'script',
		'service',
		'service_facts',
		'set_fact',
		'set_stats',
		'setup',
		'shell',
		'slurp',
		'stat',
		'subversion',
		'systemd_service',
		'sysvinit',
		'tempfile',
		'template',
		'unarchive',
		'uri',
		'user',
		'validate_argument_spec',
		'wait_for',
		'wait_for_connection',
		'yum_repository',
	]

# syntax highlighting

for module in builtin_modules
	var module_regex = 'ansible\.builtin\.' .. module
	execute 'syn match ansible_builtin_modules "' .. module_regex .. '"'
endfor

if exists("g:ansible_builtin_modules_highlight")
	execute 'highlight default link ansible_builtin_modules ' .. g:ansible_builtin_modules_highlight
else
	highlight default link ansible_builtin_modules Statement
endif

# completion

def CompleteModules(findstart: number, base: string): any
	var matches = []
	const last_string = GetStrBehindCursor()
	const prefix_end = matchend(last_string, 'ansible\.builtin\.')
	# Warning: the cursor moves after the first invokation, so don't use
	# last_string or prefix_end in the second invocation

	# remove ansible.builtin. prefix from last_string
	const partial_module = strcharpart(last_string, prefix_end)

	if findstart == 1
		if last_string == ''
			return -3
		endif

		if prefix_end == -1
			return -3
		endif

		return col('.') - strlen(partial_module) - 1
	endif

	for item in builtin_modules
		if match(item, '^' .. base) >= 0
			add(matches, item)
		endif
	endfor

	return matches
enddef

def GetStrBehindCursor(): string
	const str_start = searchpos('\s', 'bn', line('.'))[1]
	const length = col('.') - str_start - 1

	return strcharpart(getline('.'), str_start, length)
enddef


# set the custom omnifunction
setlocal completeopt=menu,menuone,noselect
setlocal omnifunc=CompleteModules
