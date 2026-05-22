/**
 * 404 页面
 */
import Link from "next/link";

export default function NotFoundPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-32 text-center">
      <h1 className="text-6xl font-bold text-gray-200 dark:text-gray-800 mb-4">
        404
      </h1>
      <p className="text-lg text-gray-500 dark:text-gray-400 mb-8">
        你找的页面不存在或已被移除。
      </p>
      <Link
        href="/"
        className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-primary-500 text-white font-medium hover:bg-primary-600 transition-colors"
      >
        ← 返回首页
      </Link>
    </div>
  );
}
