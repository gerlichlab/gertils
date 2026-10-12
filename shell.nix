{
  pkgs ? import (builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "refs/tags/23.11";
  }) {}, 
  dev ? true,
}:
let 
  py311 = pkgs.python311;
  poetryExtras = if dev then ["dev"] else [];
  poetryInstallExtras = (
    if poetryExtras == [] then ""
    else pkgs.lib.concatStrings [ " --with=" (pkgs.lib.concatStringsSep "," poetryExtras) ]
  );
in
pkgs.mkShell {
  name = "gertils-env";
  buildInputs = with pkgs; [
    poetry
    py311
    python312
  ] ++ (if dev then [
    # The pyright package from PyPI runs on Node.js; providing it here saves a download.
    pkgs.nodejs
  ] else []);
  shellHook = ''
    # To get this working on the lab machine, we need to modify Poetry's keyring interaction:
    # https://stackoverflow.com/questions/74438817/poetry-failed-to-unlock-the-collection
    # https://github.com/python-poetry/poetry/issues/1917
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
    poetry env use "${py311}/bin/python"
    poetry install -vv --sync${poetryInstallExtras}
    source "$(poetry env info --path)/bin/activate"
  '';
}
