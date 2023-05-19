{ pkgs ? import <nixpkgs> { } }:
let
  pythonPackages = with pkgs.python310Packages; [
    ipython
    pytest
    pip
    cryptography
    requests
    pdoc3
  ];
in
pkgs.mkShell rec {
  name = "pv080_crypto";

  buildInputs = with pkgs; [
    python310
  ] ++ pythonPackages;

}
