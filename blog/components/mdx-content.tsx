/**
 * MDX 内容渲染组件 —— 将 MDX 源码编译为 React 组件。
 */
"use client";

import { MDXRemote } from "next-mdx-remote/rsc";

/** 自定义 MDX 组件映射 */
const components = {
  pre: (props: React.HTMLAttributes<HTMLPreElement>) => (
    <pre className="rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 overflow-x-auto p-4 text-sm" {...props} />
  ),
  code: (props: React.HTMLAttributes<HTMLElement>) => (
    <code className="rounded bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 text-sm font-mono text-primary-700 dark:text-primary-300" {...props} />
  ),
  a: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => (
    <a
      target={props.href?.startsWith("http") ? "_blank" : undefined}
      rel="noopener noreferrer"
      className="text-primary-600 dark:text-primary-400 hover:underline"
      {...props}
    />
  ),
  table: (props: React.HTMLAttributes<HTMLTableElement>) => (
    <div className="overflow-x-auto my-6">
      <table className="min-w-full border-collapse border border-gray-200 dark:border-gray-700 text-sm" {...props} />
    </div>
  ),
  th: (props: React.HTMLAttributes<HTMLTableHeaderCellElement>) => (
    <th className="border border-gray-200 dark:border-gray-700 px-4 py-2 bg-gray-50 dark:bg-gray-900 font-semibold text-left" {...props} />
  ),
  td: (props: React.HTMLAttributes<HTMLTableDataCellElement>) => (
    <td className="border border-gray-200 dark:border-gray-700 px-4 py-2" {...props} />
  ),
  blockquote: (props: React.HTMLAttributes<HTMLQuoteElement>) => (
    <blockquote className="border-l-4 border-primary-400 pl-4 italic text-gray-600 dark:text-gray-400 my-4" {...props} />
  ),
};

interface MDXContentProps {
  source: string;
}

export function MDXContent({ source }: MDXContentProps) {
  return (
    <div className="prose prose-gray dark:prose-invert max-w-none prose-headings:scroll-mt-20 prose-img:rounded-xl">
      <MDXRemote source={source} components={components} />
    </div>
  );
}
