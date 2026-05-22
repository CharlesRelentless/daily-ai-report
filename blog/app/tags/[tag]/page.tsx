/**
 * 标签筛选页 —— 展示某标签下的所有文章
 */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getAllTags, getPostsByTag } from "@/lib/posts";
import { PostCard } from "@/components/post-card";

interface TagPageProps {
  params: { tag: string };
}

/** 静态生成所有标签页 */
export function generateStaticParams() {
  return getAllTags().map(({ tag }) => ({ tag }));
}

export function generateMetadata({ params }: TagPageProps): Metadata {
  const decodedTag = decodeURIComponent(params.tag);
  return {
    title: `标签：${decodedTag}`,
    description: `浏览标签"${decodedTag}"下的所有文章`,
  };
}

export default function TagPage({ params }: TagPageProps) {
  const decodedTag = decodeURIComponent(params.tag);
  const posts = getPostsByTag(decodedTag);

  if (posts.length === 0) notFound();

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      {/* 导航 */}
      <Link
        href="/tags"
        className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 mb-8 transition-colors"
      >
        ← 所有标签
      </Link>

      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-3">
        标签：{decodedTag}
      </h1>
      <p className="text-gray-500 dark:text-gray-400 mb-10">
        共 {posts.length} 篇文章
      </p>

      <div className="grid gap-6 sm:grid-cols-2">
        {posts.map((post) => (
          <PostCard key={post.slug} post={post} />
        ))}
      </div>
    </div>
  );
}
