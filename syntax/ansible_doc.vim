if !has('vim9script')
	finish
endif

vim9script

def LookupAnsibleDocFunc(word: string)
	var lookup_output = ''

	if ! executable('ansible-doc')
		echo "ansible-doc is not installed."
		return
	endif

	if len(ansible_keywords) == 0
		ansible_keywords = ch_read(ansible_doc_job)

		ak_dict = json_decode(ansible_keywords)
	endif

	if has_key(ak_dict, word)
		lookup_output = system('ANSIBLE_NOCOLOR=true ansible-doc -t keyword '
			.. word)
	else
		lookup_output = system('ANSIBLE_NOCOLOR=true ansible-doc ' .. word)
	endif

	echo lookup_output
enddef

var ansible_doc_job = job_start(['ansible-doc', '-j', '-t', 'keyword', '-l'],
	{'drop': 'never', 'mode': 'raw', 'err_io': 'out', 'env': {'ANSIBLE_NOCOLOR': '1'}})

var ansible_keywords = ''
var ak_dict = {}

set keywordprg=:LookupAnsibleDoc


command! -nargs=1 LookupAnsibleDoc {
	LookupAnsibleDocFunc("<args>")
}
