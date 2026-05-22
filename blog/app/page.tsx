/**
 * 首页 —— 文章列表 + 分页
 * 默认显示第 1 页，每页 6 篇。
 */
import type { Metadata } from "next";
import { getPostsPage } from "@/lib/posts";
import { PostCard } from "@/components/post-card";
import { Pagination } from "@/components/pagination";

export const metadata: Metadata = {
  title: "AI 前沿日报与开发实践",
  description: "关注 AI 前沿资讯、深度学习、自动化工具与 Next.js 开发实践。",
};

interface HomePageProps {
  searchParams: { page?: string };
}

export default function HomePage({ searchParams }: HomePageProps) {
  const currentPage = Math.max(1, parseInt(searchParams.page || "1") || 1);
  const { posts, totalPages, totalPosts } = getPostsPage(currentPage, 6);

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      {/* 页面标题 */}
      <div className="mb-10">
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100 mb-3">
          AI 前沿日报
        </h1>
        <p className="text-gray-500 dark:text-gray-400">
          共 {totalPosts} 篇文章 · 关注 AI 前沿、自动化与开发实践
        </p>
      </div>

      {/* 文章列表 */}
      {posts.length === 0 ? (
        <div className="text-center py-20 text-gray-400 dark:text-gray-600">
          <p className="text-lg mb-2">暂无文章</p>
          <p className="text-sm">新文章即将到来，敬请期待。</p>
        </div>
      ) : (
        <>
          <div className="grid gap-6 sm:grid-cols-2">
            {posts.map((post) => (
              <PostCard key={post.slug} post={post} />
            ))}
          </div>

          {/* 分页 */}
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            getPageHref={(page) => (page === 1 ? "/" : `/?page=${page}`)}
          />
        </>
      )}
    </div>
  );
}
