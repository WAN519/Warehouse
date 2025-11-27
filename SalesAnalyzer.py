import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from PromotionAdvisor import PromotionAdvisor


class SalesAnalyzer:
    def __init__(self):
        # Load environment variables first
        load_dotenv('config.env')

        # Then get the constants
        self.ANALYSIS_DAYS = int(os.environ.get('ANALYSIS_DAYS', 30))
        self.LOW_SALES_THRESHOLD = int(os.environ.get('LOW_SALES_THRESHOLD', 10))

        # Database configuration
        DB_CONFIG = {
            'host': os.environ.get('DB_HOST'),
            'database': os.environ.get('DB_DATABASE'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'port': int(os.environ.get('DB_PORT', 5432)),
            'ssl_ca': os.environ.get('DB_SSL_CA'),
            'ssl_verify_cert': bool(os.environ.get('DB_SSL_VERIFY_CERT')) == True
        }

        self.config = DB_CONFIG.copy()
        self.config['use_pure'] = True

    def _get_connection(self):
        """Connect to database"""
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"Connection failed: {e}")
            return None

    def get_slow_moving_products(self, days=None):
        """
        Search for slow-moving products

        Return type:
        [
            {
                'supplier_id': 'S00000001',
                'product_id': 'P00000001',
                'product_name': 'Product Name',
                'type': 'Category',
                'price': 99.99,
                'stock_quantity': 450,
                'supply_quantity': 500,
                'sell_through_rate': 0.10,
                'days_in_stock': 30,
                'warehouse_id': 'W00000001'
            },
            ...
        ]
        """
        if days is None:
            days = self.ANALYSIS_DAYS

        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            if not conn:
                return None

            cursor = conn.cursor(dictionary=True)

            # Fixed SQL query based on your actual table structure
            query = """
            SELECT 
                gs.supplier_id,
                gs.product_id,
                p.product_name,
                p.type,
                p.price,
                p.manufacturer,
                sr.storequantity as stock_quantity,
                gs.quantity as supply_quantity,
                gs.warehouse_id,
                gs.supply_time,
                DATEDIFF(CURDATE(), DATE(gs.supply_time)) as days_in_stock,
                ROUND((gs.quantity - sr.storequantity) / gs.quantity, 2) as sell_through_rate
            FROM good_supply gs
            LEFT JOIN store_records sr 
                ON gs.warehouse_id = sr.warehouse_id 
                AND gs.product_id = sr.product_id
            LEFT JOIN products p
                ON gs.product_id = p.product_id
            WHERE DATEDIFF(CURDATE(), DATE(gs.supply_time)) >= %s
                AND (gs.quantity - sr.storequantity) / gs.quantity < 0.2
                AND sr.storequantity > 100
            ORDER BY sr.storequantity DESC, sell_through_rate ASC
            LIMIT 50
            """

            cursor.execute(query, (self.LOW_SALES_THRESHOLD,))
            results = cursor.fetchall()

            # Convert datetime to string
            for row in results:
                if row.get('supply_time'):
                    row['supply_time'] = row['supply_time'].strftime('%Y-%m-%d %H:%M:%S')

            return results

        except Error as e:
            print(f"Query failed: {e}")
            print(f"Error details: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_category_performance(self):
        """
        Get sales performance by category

        Return type:
        [
            {
                'category': 'Electronics',
                'total_products': 50,
                'slow_moving_count': 15,
                'slow_moving_percentage': 30.0,
                'avg_stock': 250
            },
            ...
        ]
        """
        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            if not conn:
                return None

            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT 
                p.type as category,
                COUNT(DISTINCT p.product_id) as total_products,
                AVG(sr.storequantity) as avg_stock,
                SUM(CASE 
                    WHEN sr.storequantity > 100 THEN 1 
                    ELSE 0 
                END) as high_stock_count
            FROM products p
            LEFT JOIN store_records sr ON p.product_id = sr.product_id
            GROUP BY p.type
            ORDER BY high_stock_count DESC
            """

            cursor.execute(query)
            results = cursor.fetchall()

            # Calculate percentages
            for row in results:
                if row['total_products'] > 0:
                    row['high_stock_percentage'] = round(
                        (row['high_stock_count'] / row['total_products']) * 100, 2
                    )
                else:
                    row['high_stock_percentage'] = 0.0

                # Round avg_stock
                if row['avg_stock']:
                    row['avg_stock'] = round(row['avg_stock'], 2)

            return results

        except Error as e:
            print(f"Query failed: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def format_data_for_ai(self):
        """Format data for AI analysis"""
        slow_products = self.get_slow_moving_products()
        category_performance = self.get_category_performance()

        if not slow_products:
            return None

        # Build report for AI
        report = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'analysis_period': f'Products in stock for {self.ANALYSIS_DAYS}+ days',
            'low_sales_threshold': f'Less than {self.LOW_SALES_THRESHOLD}% sold',
            'slow_moving_products': slow_products,
            'category_performance': category_performance,
            'total_slow_products': len(slow_products)
        }

        return report

    def get_product_sales_history(self, product_id, days=30):
        """
        Get sales history for a specific product

        Args:
            product_id: Product ID
            days: Number of days to look back

        Returns:
            List of sales records
        """
        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            if not conn:
                return None

            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT 
                i.order_id,
                i.orderquantity,
                o.order_time,
                i.status,
                i.warehouse_id
            FROM inform i
            JOIN orders o ON i.order_id = o.order_id
            WHERE i.product_id = %s
                AND o.order_time >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ORDER BY o.order_time DESC
            """

            cursor.execute(query, (product_id, days))
            results = cursor.fetchall()

            # Convert datetime
            for row in results:
                if row.get('order_time'):
                    row['order_time'] = row['order_time'].strftime('%Y-%m-%d %H:%M:%S')

            return results

        except Error as e:
            print(f"Query failed: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


# Example usage
    def test(self):
        analyzer = SalesAnalyzer()

        category_performance = analyzer.get_category_performance()

        if category_performance:
            for cat in category_performance:
                print(f"\n{cat['category']}:")
                print(f"  Total Products: {cat['total_products']}")
                print(f"  Avg Stock: {cat['avg_stock']:.0f}")
                print(f"  High Stock Items: {cat['high_stock_count']} ({cat['high_stock_percentage']:.1f}%)")

         # Test full report

        report = analyzer.format_data_for_ai()

        return report