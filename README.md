# Emulon X community skins

Skins for [Emulon X](https://github.com/KiruTheProot-Creative/EmulonX), made by the community in **Emulon X SD** (the skin designer).

## Getting skins

The easiest way is the **Emulon X Hub**: open the **EMULON SKINS** tab, pick a skin and click **Get this skin**.
It goes straight into your skins folder, and you choose it in Emulon X under **Settings > Customization**.

You can also download a skin's `skin.emxd` from the `skins` folder here and drop it onto the Emulon X window.

## Sharing your skin

In the **Emulon X Hub**, click **Submit skin**, sign in with your GitHub account and pick your `.emxd` file.
The Hub takes care of everything else: it makes a preview picture, checks the file and sends it in for review.
Once it's approved, it shows up in everyone's Hub.

Prefer to do it by hand? Open a pull request that adds one folder, `skins/<your-skin-name>/`, with:

| File | What it is |
|---|---|
| `skin.emxd` | your skin, saved from Emulon X SD (up to 20 MB) |
| `preview.png` | a picture of Emulon X wearing it (up to 2 MB) |
| `info.json` | `{ "name": "...", "author": "...", "description": "...", "version": "1.0" }` |

The folder name uses small letters, numbers and dashes only (for example `deep-blue`).
An automatic check runs on every submission and says what to fix if something's wrong.

## Rules

- Only your own work, or work you're allowed to share. Pictures, textures and fonts inside the skin must be free to share too.
- No logos or brand names you don't own.
- Keep it friendly: nothing hateful, violent or adult.

By submitting a skin you agree that it can be shared and used by everyone under the
[Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) license (people may use and change it, as long as they credit you).

## For the Hub

`index.json` lists every skin. It's rebuilt automatically whenever a skin is added or changed - don't edit it by hand.
