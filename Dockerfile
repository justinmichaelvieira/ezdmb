# Use amake/innosetup on the public docker repo as a base
FROM amake/innosetup

# See: https://github.com/amake/innosetup-docker/issues/7#issuecomment-1312605128
USER root
RUN chown -R root /home

# Copy iss script for build, and files to bundle
COPY ezdmb-installer.iss ./ezdmb-installer.iss
COPY artifacts/icon.ico ./icon.ico
COPY artifacts/.version ./.version

CMD ["ezdmb-installer.iss"]
