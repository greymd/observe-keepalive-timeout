# observe-keepalive-timeout

This is a simple script to observe keepalive timeout.

The most reliable way to check the keepalive timeout seconds is to observe actual TCP connection status.

The script sends a HTTP request to the specified URL but does not actively close the connection but wait for the connection to be closed by the server. Then, the script observes the connection status using `ss` command.

## Example

```
$ python3 ./main.py checkip.amazonaws.com
⋮
⋮
Waiting for 1 seconds, connection = ESTAB
Waiting for 2 seconds, connection = ESTAB
⋮
Waiting for 13 seconds, connection = ESTAB
Waiting for 14 seconds, connection = ESTAB
Waiting for 15 seconds, connection = ESTAB
Connection is in CLOSE-WAIT state
```
=> *keepalive timeout is around 15 seconds* on `checkip.amazonaws.com`. We can see that the connection is half closed (CLOSE-WAIT) after 15 seconds.

## Usage (For Linux)

Install `ss` and `python3` if you don't have them.
And run the following command.

```
$ python3 ./main.py example.com
```

If you want to run the script in a Docker container, run the following command.

```
$ docker run -it -v $PWD:/root --rm nicolaka/netshoot python3 ./main.py example.com
```

## Usage (For macOS)

Use `docker` as instructed above since macOS does not have `ss` command. So, you need to run the script in a container.

FYI: `finch` command is also available in macOS. You can use `finch` instead of `docker`.

```
$ brew install finch
$ finch vm start
$ finch run -it -v $PWD:/root --rm nicolaka/netshoot python3 ./main.py example.com
```

