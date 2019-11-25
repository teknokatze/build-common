statusmsg()
{
    ${runcmd} echo "${tab}$@" | tee -a "${results}"
}

infomsg()
{
    if [ x$verbosity = x1 ]; then
	statusmsg "INFO:${tab}$@"
    fi
}

warningmsg()
{
    statusmsg "WARNING:${tab}$@"
}

errormsg()
{
    statusmsg "ERROR:${tab}$@"
}

linemsg()
{
    statusmsg "========================================="
}
