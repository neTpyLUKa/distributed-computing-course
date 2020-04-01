FROM    golang:alpine AS builder
WORKDIR /usr/src/app/
COPY    go.mod .
COPY    go.sum .
RUN     go mod download
COPY    . .
RUN     go build -o /app .

FROM alpine AS production
RUN  apk update && apk add bash ca-certificates libc6-compat && rm -rf /var/cache/apk/*
COPY --from=builder /app ./
COPY utils utils