"""CLI entry point for Stock Agent"""

import sys
import argparse
from stock_agent.services.stock_service import StockService
from stock_agent.services.market_data_service import MarketDataService
from stock_agent.services.alert_service import AlertService
from stock_agent.repositories.stock_repository import JSONStockRepository
from stock_agent.config import get_settings


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Stock Agent - Autonomous Stock Monitoring System"
    )
    parser.add_argument(
        "command",
        choices=["analyze", "track", "list", "run"],
        help="Command to execute"
    )
    parser.add_argument("--symbol", help="Stock symbol (e.g., TCS.NS, AAPL)")
    parser.add_argument("--buy-price", type=float, help="Buy price")
    parser.add_argument("--target-price", type=float, help="Target price")
    
    args = parser.parse_args()
    
    # Initialize services
    settings = get_settings()
    market_service = MarketDataService()
    alert_service = AlertService(settings)
    repository = JSONStockRepository(settings.data_file_path)
    stock_service = StockService(market_service, alert_service, repository)
    
    try:
        if args.command == "analyze":
            if not all([args.symbol, args.buy_price, args.target_price]):
                print("Error: --symbol, --buy-price, and --target-price are required for analyze")
                sys.exit(1)
            
            result = stock_service.analyze_stock(
                args.symbol,
                args.buy_price,
                args.target_price
            )
            print(f"\n{result.decision}")
            print(f"Symbol: {result.symbol}")
            print(f"Current Price: ${result.current_price:.2f}")
            print(f"Profit: ${result.profit:.2f} ({result.profit_percent:.2f}%)")
            
        elif args.command == "track":
            if not all([args.symbol, args.buy_price, args.target_price]):
                print("Error: --symbol, --buy-price, and --target-price are required for track")
                sys.exit(1)
            
            stock_service.track_stock(args.symbol, args.buy_price, args.target_price)
            print(f"✅ {args.symbol} added to tracking list")
            
        elif args.command == "list":
            stocks = stock_service.get_tracked_stocks()
            if not stocks:
                print("No stocks being tracked")
            else:
                print(f"\n📊 Tracking {len(stocks)} stock(s):\n")
                for stock in stocks:
                    print(f"  • {stock.symbol}: ${stock.buy_price:.2f} → ${stock.target_price:.2f}")
                    
        elif args.command == "run":
            results = stock_service.run_agent()
            print(f"\n🤖 Agent analyzed {len(results)} stock(s)\n")
            for result in results:
                print(f"{result.decision} - {result.symbol}: ${result.current_price:.2f}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
