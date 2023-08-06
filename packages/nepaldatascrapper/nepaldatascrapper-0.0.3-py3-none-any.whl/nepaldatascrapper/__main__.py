from nepse import NEPSE

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="scraps the current value of the share")
    parser.add_argument("symbol",type=str,help="stock symbol")
    args = parser.parse_args()
    if args.symbol:
        nepse = NEPSE()
        print(nepse.getSharePrice(args.symbol))
