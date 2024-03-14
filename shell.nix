{
  pkgs ? import (builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "refs/tags/23.11";
  }) {}, 
  dev ? true,
}:
let 
  py310 = pkgs.python310;
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
    py310
    python311
    python312
  ];
  shellHook = ''
    # To get this working on the lab machine, we need to modify Poetry's keyring interaction:
    # https://stackoverflow.com/questions/74438817/poetry-failed-to-unlock-the-collection
    # https://github.com/python-poetry/poetry/issues/1917
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
    poetry env use "${py310}/bin/python"
    export LD_LIBRARY_PATH="${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib"
    poetry install -vv --sync${poetryInstallExtras}
    source "$(poetry env info --path)/bin/activate"
  '';
}
