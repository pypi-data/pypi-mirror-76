frattlesnake
===

<img class="snake" src="https://cdn.coldfront.net/thekolwiki/images/a/a6/Snakeboss2.gif" style="height:1.5em" />

`frattlesnake` is a bridge and library from KoLmafia's Java environment to a Python environment. It is extremely 🚧 under construction 🚧 but it is usable!

For now just clone this repo and play with the examples. It will even download the latest `kolmafia.jar` for you to hook into.

Requirements
====

* Python 3.8+
* I am running the same version of Java that was used to compile the JAR on the build server just in case.

Development
===

```shell
poetry install
```

to install our dependencies and then just run your file! You may need to manually specify the path to your `libjvm.so`. For example, on my machine I needed to run

```shell
JVM_PATH=~/.jenv/versions/1.8/jre/lib/amd64/server/libjvm.so python ./example.py
```

because I use `jEnv` to manage my Java versions. And that path is totally different in my Java 11 directory so it's a pain for now.
