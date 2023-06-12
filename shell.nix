{
  pkgs ? import (builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "nixos-22.11";
    rev = "96e18717904dfedcd884541e5a92bf9ff632cf39";
  }) {}
}:
let
  python310WithPoetry = (
    pkgs.python310.withPackages (pypkgs: with pypkgs; [
      poetry
    ])
  );
in
pkgs.mkShell {
  name = "gertils-env";
  buildInputs = with pkgs; [
    python38
    python39
    python310WithPoetry
    python311
  ];
  shellHook = ''
    poetry env use "${python310WithPoetry}/bin/python"
    poetry install --sync --with=dev
    source "$(poetry env info --path)/bin/activate"
  '';
}
