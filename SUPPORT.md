# Support

## Where to get help

| Channel | Use it for |
|---------|------------|
| [GitHub Discussions](https://github.com/aryaminus/astro/discussions) | Questions, ideas, "how do I...?" |
| [GitHub Issues](https://github.com/aryaminus/astro/issues/new/choose) | Bug reports, feature requests |
| [Security Advisory](https://github.com/aryaminus/astro/security/advisories/new) | Security vulnerabilities (private) |
| [Documentation](https://github.com/aryaminus/astro#documentation) | Reference docs |
| Email `support@aryaminus.dev` | Private / commercial inquiries |

## Before opening an issue

1. Search [existing issues](https://github.com/aryaminus/astro/issues)
2. Check the [docs](README.md) and [skill README](skills/astrology/README.md)
3. Try the latest release — your bug may already be fixed
4. Run with `ASTRO_LOG_LEVEL=DEBUG` and include the relevant log lines

## Common questions

### "Is astrology real?"
This project treats astrology as a **tradition**, not a science. The engine
performs astronomical math; the interpretations are grounded in classical
rulesets. Nothing in this repo claims supernatural efficacy.

### "How do I host this on my own server?"
See [README.md → Cloud hosting](README.md#cloud-hosting). The
`docker-compose.yml` and `render.yaml` cover the common cases.

### "Can I use this commercially?"
Yes — MIT license. Set `ASTRO_API_KEY` to gate access and you can charge
for it. The engine is honest about the tradition it's grounded in; we
encourage that honesty in any commercial use.

### "How do I add a new calculation mode?"
See [CONTRIBUTING.md](CONTRIBUTING.md). The 4-surface rule applies.

### "The chart I got is wrong"
The engine is **~1-2 arcmin accurate** with the builtin (pure-Python)
backend. For sub-arcsecond precision, install Swiss Ephemeris:
`pip install pyswisseph`. The engine auto-upgrades.
