# mitmproxy Addon: Geometry Dash rewards

_This script is an addon for [mitmproxy](https://www.mitmproxy.org/)._  

Automatically intercept, decode, and modify GD's requests (and their responses) to the official servers for daily chest contents.  

**Tested with**: GD 2.2.143 on Android  


## Usage

The script can be loaded as a mitmproxy addon by using:
```shell
# for example with mitmweb
mitmweb -s addonGDRewards.py
```

When in use, the script automatically re-writes the response from the GD server, to the values set at the end of `addonGDRewards.py`.

### Configuring values

Each chest has 4 different slots for items:
1. Any amount of orbs
2. Any amount of gems
3. One special item
4. One special item

See [Item IDs](#item-ids) below for the IDs of special items.

The values, which both chests are set to, are defined at the end of `addonGDRewards.py`:
```python
addons = [
    GDRewards(
        "100",  # orbs
        "10",   # gems
        "6",    # item 1
        "6",    # item 2
        False   # modify time (see time modification below)
    )
]
```

### Item IDs


The IDs of special items are:

| ID | Item      |
|----|-----------|
| 1  | Fire      |
| 2  | Ice       |
| 3  | Poision   |
| 4  | Shadow    |
| 5  | Lava      |
| 6  | Demon key |
| 10 | Earth     |
| 11 | Blood     |
| 12 | Metal     |
| 13 | Light     |
| 14 | Soul      |


### Time modification

Apart from modifying the contents of chests, changing chest-cooldowns (time until chest can be opened) is also semi-supported.
See usage above on how to enable it.  

However, this feature comes with the limitation of desyncing the server with the client, as both keep track of how many chests you have opened.
Therefore, you will only be able to fast-forward once, and afterward have to wait the standard cooldown.
Additionally, the first chest you open after disabling the script will fail to work, since server and client are still desynced by one chest.


## Implementation details

When fetching daily rewards, GD queries `www.boomlings.com/database/getGJRewards.php`, which responds with an unlabeled array representing information about the client and their respective chests:

| Index | Modified by script             | Description                            |
|-------|--------------------------------|----------------------------------------|
| 0     | No                             | Random sequence of 5 characters        |
| 1     | No                             | Player ID                              |
| 2     | No                             | Check number (usage unclear)           |
| 3     | No                             | Device UUID                            |
| 4     | No                             | Account UUID                           |
| 5     | Yes (when using `modify_time`) | Small chest time remaining             |
| 6     | Yes                            | Small chest's rewards                  |
| 7     | Yes (when using `modify_time`) | Count of small chests claimed          |
| 8     | Yes (when using `modify_time`) | Large chest time remaining             |
| 9     | Yes                            | Large chest's rewards                  |
| 10    | Yes (when using `modify_time`) | Count of large chests claimed          |
| 11    | No                             | rewardType (used when opening a chest) |


### Encryption keys

GD obfuscates the content of the response by using:
- XORing
- Appending special salts

Corresponding to the version used to test the addon, following keys are used:

| Key          | Usage  |
|--------------|--------|
| 59182        | XORing |
| pC26fpYaQCtg | Salt   |

These may change in future versions of GD and can be adjusted at the top of `addonGDRewards.py`.


## References

 - Unofficial GD documentation: [Link 1](https://wyliemaster.github.io/gddocs/#/), [Link 2](https://gddocs.omgrod.me/)
 - [dashtools](https://github.com/A-Zalt/dashtools/tree/master) (for decoding logic)
 - [GMDPrivateServer](https://github.com/Cvolton/GMDprivateServer) (third-party implementation of the endpoint)
