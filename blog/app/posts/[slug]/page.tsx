/**
 * 文章详情页 —— 使用 compileMDX 在服务端渲染 MDX 内容
 */
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { compileMDX } from "next-mdx-remote/rsc";
import { getPostBySlug, getAllPosts } from "@/lib/posts";

/** 自定义 MDX 组件 */
const mdxComponents = {
  pre: (props: any) => (
    <pre className="rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 overflow-x-auto p-4 text-sm" {...props} />
  ),
  code: (props: any) => (
    <code className="rounded bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 text-sm font-mono text-primary-700 dark:text-primary-300" {...props} />
  ),
  a: (props: any) => (
    <a target={props.href?.startsWith("http") ? "_blank" : undefined} rel="noopener noreferrer" className="text-primary-600 dark:text-primary-400 hover:underline" {...props} />
  ),
  table: (props: any) => (
    <div className="overflow-x-auto my-6"><table className="min-w-full border-collapse border border-gray-200 dark:border-gray-700 text-sm" {...props} /></div>
  ),
  blockquote: (props: any) => (
    <blockquote className="border-l-4 border-primary-400 pl-4 italic text-gray-600 dark:text-gray-400 my-4" {...props} />
  ),
};

interface PostPageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return getAllPosts().map((p) => ({ slug: p.slug }));
}

export function generateMetadata({ params }: PostPageProps): Metadata {
  const post = getPostBySlug(params.slug);
  if (!post) return { title: "文章未找到" };
  return {
    title: post.frontmatter.title,
    description: post.frontmatter.summary,
    keywords: post.frontmatter.tags,
    openGraph: {
      title: post.frontmatter.title,
      description: post.frontmatter.summary,
      type: "article",
      publishedTime: post.frontmatter.date,
      tags: post.frontmatter.tags,
    },
  };
}

export default async function PostPage({ params }: PostPageProps) {
  const post = getPostBySlug(params.slug);
  if (!post) notFound();

  const { frontmatter, readingTime } = post;
  const dateObj = new Date(frontmatter.date + "T00:00:00+08:00");
  const dateFormatted = dateObj.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  // 在服务端编译 MDX
  const { content } = await compileMDX({
    source: post.content,
    components: mdxComponents,
  });

  return (
    <article className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
      <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 mb-8 transition-colors">
        ← 返回首页
      </Link>

      <header className="mb-10">
        <div className="flex flex-wrap gap-2 mb-4">
          {frontmatter.tags.map((tag) => (
            <Link key={tag} href={`/tags/${tag}`}
              className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 hover:bg-primary-100 transition-colors">
              {tag}
            </Link>
          ))}
        </div>

        <h1 className="text-2xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100 leading-tight mb-4">
          {frontmatter.title}
        </h1>

        <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
          <time dateTime={frontmatter.date}>{dateFormatted}</time>
          <span>·</span>
          <span>阅读约 {readingTime} 分钟</span>
          {frontmatter.author && (<><span>·</span><span>{frontmatter.author}</span></>)}
        </div>
      </header>

      {/* 渲染编译后的 MDX 内容 */}
      <div className="prose prose-gray dark:prose-invert max-w-none prose-headings:scroll-mt-20 prose-img:rounded-xl prose-pre:!bg-gray-50 dark:prose-pre:!bg-gray-900 prose-code:before:content-none prose-code:after:content-none">
        {content}
      </div>

      <footer className="mt-16 pt-8 border-t border-gray-100 dark:border-gray-800">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
          ← 返回首页
        </Link>
      </footer>
    </article>
  );
}
