try:  # Python 2
    from bed import run
except ImportError:  # Python 3
    from .bed import run

def main():
    run()

if __name__ == "__main__":
    run()