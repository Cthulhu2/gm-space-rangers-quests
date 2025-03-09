# Gemini capsule with Space Ranger Quests

* `/borrowed/qm/` -- dir for quests from "Space Ranges"
* `/srqmplayer/` -- python port the quest player from the [space-rangers-quest][0] repo
* `/content/` -- static content, quest images/sounds/tracks
* `99_gm_mod_srquests.py` -- [GmCapsule][1] server extension
* [Project Gemini][2]

[0]: https://github.com/roginvs/space-rangers-quest
[1]: https://codeberg.org/skyjake/gmcapsule
[2]: https://geminiprotocol.net/

Create migration:
```shell
$ pw_migrate create --auto \
  --database "sqlite:/./users/gmsrq.sqlite" \
  --directory ./gmsrq/migrations \
  <migration_name>
```
Migrate:
```shell
$ pw_migrate migrate \
  --database "sqlite:/./users/gmsrq.sqlite" \ 
  --directory ./gmsrq/migrations
```
Rollback:
```shell
$ pw_migrate rollback \
  --database "sqlite:/users/gmsrq.sqlite" \
  --directory ./gmsrq/migrations/ \
  --count 1
```

Localization:
```shell
$ pybabel extract --project=gmsrq --version=0.1 -o locale/gmsrq.pot \
  srqmplayer/*.py gmsrq/*.py
$ pybabel init -D gmsrq -i locale/gmsrq.pot -d locale -l ru
$ pybabel update -D gmsrq -i locale/gmsrq.pot -d locale
$ pybabel compile -D gmsrq -d locale
```