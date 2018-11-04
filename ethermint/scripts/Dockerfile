FROM dxsdk/chain:develop as builder

# 1) copy personal config
ENV HOME "/root"
COPY temp/github.com ${HOME}/go/src/github.com

# 2) build ethermint
RUN cd ${HOME}/go/src/github.com/tendermint/ethermint                                               &&\
    make install

# 3) build tendermint
RUN cd ${HOME}/go/src/github.com/tendermint/tendermint                                              &&\
    make install

################################################################################
FROM alpine:3.7
# 0) environment variable
ENV HOME "/root"
# 1) add bash and tzdata
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories                   &&\
    apk update                                                                                      &&\
    apk add --no-cache tzdata bash                                                                  &&\
    rm -rf /var/cache/apk/

# 2) copy released binaries
COPY --from=builder ${HOME}/go/bin /dxsdk/bin
ENV PATH "${PATH}:/dxsdk/bin"

# 3) entrypoint
ENV DATADIR /data
CMD ethermint --datadir ${DATADIR} --with-tendermint init ${DATADIR}/genesis.json                   &&\
    ethermint --datadir ${DATADIR} --with-tendermint --rpcapi eth,net,web3,personal,admin --rpc --rpcaddr=0.0.0.0
