# Use amake/innosetup on the public docker repo as a base
FROM amake/innosetup

# Copy iss script for build, and files to bundle
COPY ./ezdmb-installer.iss ./ezdmb-installer.iss
COPY ./icon.ico /icon.ico
COPY ./ezdmb-x32.exe ./ezdmb-x32.exe
COPY ./ezdmb-x64.exe ./ezdmb-x64.exe
COPY ./dmb_config.json ./dmb_config.json
COPY ./.version ./.version
COPY ./ezdmb/ ./ezdmb/
