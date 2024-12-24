{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
	packages = with pkgs; [
    	python312
		python312Packages.requests
  	];

	shellHook = ''
		python main.py
	'';
}
