print_version()
{
    GNUNET_ARM_VERSION=`gnunet-arm -v | awk '{print $2 " " $3}'`
    echo ${progname} $GNUNET_ARM_VERSION
}
