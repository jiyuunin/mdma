# MDMA The Game

**MDMA The Game** is a simple game written in the [Python][] language using
[pygame][], based on [Merchant Moe][] MDMA (Moe's Dynamic Maker Awards)
initiative.

The goal is to accumulate a maximum of **MOE** in four weeks (corresponding to
about 13 seconds in real time) by constantly rebalancing the position in the
**MOE/MNT** liquidity pool, using the left and right arrow keys, in order to be
in the reward range.

https://github.com/jiyuunin/mdma/assets/89147566/4c244a89-dc79-4ac5-a772-53c676ac7eed

The game is available on GitHub in [the releases section][Release] or can
be generated using [PyInstaller][] by downloading [the archive of this
repository][Archive repository], installing [Tox][] and running the following
command in the project directory:

```console
$ tox -e pkg
```

The executable `mdma` is generated in the `dist` folder.

[Archive repository]: https://github.com/jiyuunin/mdma/archive/refs/heads/master.zip
[Merchant Moe]: https://merchantmoe.com
[Python]: https://www.python.org
[PyInstaller]: https://pyinstaller.org
[pygame]: https://www.pygame.org
[Release]: https://github.com/jiyuunin/mdma/releases/tag/0.1.0
[Tox]: https://tox.wiki
