/**
 * 全局页脚
 */
export function Footer() {
  return (
    <footer className="border-t border-gray-100 dark:border-gray-800 mt-20">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 text-center">
        <p className="text-sm text-gray-500 dark:text-gray-500">
          © {new Date().getFullYear()} 小悟的博客 · 由{" "}
          <a
            href="https://nextjs.org"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-500 hover:text-primary-600 transition-colors"
          >
            Next.js
          </a>{" "}
          驱动 · 内容源自{" "}
          <a
            href="https://aihot.virxact.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-500 hover:text-primary-600 transition-colors"
          >
            AI HOT
          </a>
        </p>
      </div>
    </footer>
  );
}
