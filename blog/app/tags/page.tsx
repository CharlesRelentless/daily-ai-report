/**
 * 标签汇总页 —— 展示所有标签及其文章数
 */
import type { Metadata } from "next";
import Link from "next/link";
import { getAllTags } from "@/lib/posts";

export const metadata: Metadata = {
  title: "标签",
  description: "按标签浏览所有文章",
};

export default function TagsPage() {
  const tags = getAllTags();

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-3">
        标签
      </h1>
      <p className="text-gray-500 dark:text-gray-400 mb-10">
        共 {tags.length} 个标签 · 点击查看相关文章
      </p>

      {tags.length === 0 ? (
        <p className="text-gray-400 dark:text-gray-600">暂无标签</p>
      ) : (
        <div className="flex flex-wrap gap-3">
          {tags.map(({ tag, count }) => (
            <Link
              key={tag}
              href={`/tags/${tag}`}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all group"
            >
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300 group-hover:text-primary-700 dark:group-hover:text-primary-300">
                {tag}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/30 group-hover:text-primary-600">
                {count}
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
