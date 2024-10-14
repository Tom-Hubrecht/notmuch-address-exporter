{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
}:

{
  devShell = pkgs.mkShell {
    name = "nae-dev";

    packages = [
      (pkgs.python3.withPackages (ps: [
        ps.ipython
        ps.notmuch2
      ]))
    ];
  };
}
