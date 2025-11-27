# scheduler.py
import schedule
import time
from datetime import datetime
from SalesAnalyzer import SalesAnalyzer
from PromotionAdvisor import PromotionAdvisor
from config import ANALYSIS_TIME


class PromotionScheduler:
    """Sales scheduler"""

    def __init__(self):
        self.analyzer = SalesAnalyzer()
        self.advisor = PromotionAdvisor()

    def run_analysis(self):
        """执行一次完整的分析"""
        print(f"\n{'=' * 80}")
        print(f"开始执行促销分析 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 80}\n")

        # 1. 获取销售数据
        print("📊 正在从数据库获取销售数据...")
        sales_data = self.analyzer.format_data_for_ai()

        if not sales_data:
            print("❌ 未能获取到数据或没有滞销商品")
            return

        print(f"✓ 找到 {sales_data['total_slow_products']} 个滞销商品\n")

        # 2. 显示滞销商品概览
        print("滞销商品概览:")
        for i, product in enumerate(sales_data['slow_moving_products'][:5], 1):
            print(
                f"{i}. {product['product_name']} - 销量: {product['total_sales']}件 - 库存: {product['stock_quantity']}件")

        if sales_data['total_slow_products'] > 5:
            print(f"... 还有 {sales_data['total_slow_products'] - 5} 个商品\n")

        # 3. 调用AI生成促销方案
        print("\n🤖 正在使用AI分析并生成促销方案...")
        promotion_plan = self.advisor.generate_promotion_plan(sales_data)

        if promotion_plan:
            print("\n" + "=" * 80)
            print("AI促销方案建议")
            print("=" * 80 + "\n")
            print(promotion_plan)

            # 4. 保存结果到文件
            self.save_report(sales_data, promotion_plan)

        else:
            print("❌ AI分析失败")

        print(f"\n{'=' * 80}")
        print(f"分析完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 80}\n")

    def save_report(self, sales_data, promotion_plan):
        """保存分析报告到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"promotion_report_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"促销分析报告\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"分析周期: {sales_data['analysis_period']}\n")
                f.write(f"{'=' * 80}\n\n")
                f.write(promotion_plan)

            print(f"\n✓ 报告已保存至: {filename}")

        except Exception as e:
            print(f"保存报告失败: {e}")

    def start(self):
        """启动定时任务"""
        print(f"🚀 促销分析系统已启动")
        print(f"📅 每天 {ANALYSIS_TIME} 自动执行分析")
        print(f"💡 你也可以按 Ctrl+C 停止程序\n")

        # 设置定时任务
        schedule.every().day.at(ANALYSIS_TIME).do(self.run_analysis)

        # 可选：立即执行一次
        print("是否立即执行一次分析? (y/n): ", end='')
        choice = input().strip().lower()
        if choice == 'y':
            self.run_analysis()

        # 保持运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    scheduler = PromotionScheduler()
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n\n👋 程序已停止")