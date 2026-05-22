/**
 * 文章卡片组件 —— 用于首页和标签筛选页
 */
import Link from "next/link";
import type { PostListItem } from "@/types/post";

interface PostCardProps {
  post: PostListItem;
}

export function PostCard({ post }: PostCardProps) {
  const { slug, frontmatter, readingTime } = post;
  const dateObj = new Date(frontmatter.date + "T00:00:00+08:00");
  const dateFormatted = dateObj.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <article className="group border border-gray-100 dark:border-gray-800 rounded-xl p-5 sm:p-6 hover:border-primary-200 dark:hover:border-primary-800 hover:shadow-md transition-all duration-200 bg-white dark:bg-gray-900">
      {/* 标签 */}
      <div className="flex flex-wrap gap-2 mb-3">
        {frontmatter.tags.map((tag) => (
          <Link
            key={tag}
            href={`/tags/${tag}`}
            className="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors"
          >
            {tag}
          </Link>
        ))}
      </div>

      {/* 标题 */}
      <Link href={`/posts/${slug}`}>
        <h2 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors mb-2 line-clamp-2">
          {frontmatter.title}
        </h2>
      </Link>

      {/* 摘要 */}
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-3 leading-relaxed">
        {frontmatter.summary}
      </p>

      {/* 底部信息 */}
      <div className="flex items-center justify-between text-xs text-gray-400 dark:text-gray-500">
        <span>{dateFormatted}</span>
        <span>阅读约 {readingTime} 分钟</span>
      </div>
    </article>
  );
}
