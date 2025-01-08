# Use amake/innosetup on the public docker repo as a base
FROM amake/innosetup

# Copy iss script for build, and files to bundle
COPY ./ezdmb-installer.iss ./work/ezdmb-installer.iss
COPY ./icon.ico ./work/icon.ico
COPY ./dmb_config.json ./work/dmb_config.json
COPY ./.version ./work/.version
