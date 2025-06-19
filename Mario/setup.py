import subprocess
import sys
import pkg_resources
import warnings

warnings.filterwarnings("ignore", category=pkg_resources.PkgResourcesDeprecationWarning)

def install_if_needed(package_name: str, min_version: str = None):
    try:
        distribution: pkg_resources.Distribution = pkg_resources.get_distribution(package_name)
        if min_version is not None:
            current_version: pkg_resources.Version = distribution.parsed_version
            required_version: pkg_resources.Version = pkg_resources.parse_version(min_version)
            if current_version < required_version:
                print(f"{package_name} version {current_version} is too old. Upgrading to {min_version}...")
                install_target = f"{package_name}>={min_version}" if min_version else package_name
                subprocess.check_call([sys.executable, "-m", "pip", "install", install_target])
        print(f"{package_name} {distribution.version} is installed")
    except pkg_resources.DistributionNotFound:
        print(f"Installing {package_name}...")
        install_target = f"{package_name}>={min_version}" if min_version else package_name
        subprocess.check_call([sys.executable, "-m", "pip", "install", install_target])
    except Exception as e:
        print(f"Failed to install {package_name}: {e}")

def setup():
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
        install_if_needed("pip")
        for index, requirement in enumerate(requirements):
            data = requirement.split(" ")
            if len(data) == 1:
                try:
                    install_if_needed(data[0])
                except subprocess.CalledProcessError as e:
                    print(f"invalid requirement: {requirement}" , f"line: {index + 1}")
            elif len(data) == 2:
                try:
                    install_if_needed(data[0], data[1])
                except subprocess.CalledProcessError as e:
                    print(f"invalid requirement: {requirement}", f"line: {index + 1}")
            else:
                raise ValueError(f"Invalid requirement: {requirement}", f"line: {index + 1}")

if __name__ == "__main__":
    setup()