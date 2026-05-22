/**
 * 分页组件
 */
import Link from "next/link";

interface PaginationProps {
  /** 当前页码 */
  currentPage: number;
  /** 总页数 */
  totalPages: number;
  /** 生成链接的函数（接收页码，返回 href） */
  getPageHref: (page: number) => string;
}

export function Pagination({ currentPage, totalPages, getPageHref }: PaginationProps) {
  if (totalPages <= 1) return null;

  const pages: (number | "...")[] = [];
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
      pages.push(i);
    } else if (pages[pages.length - 1] !== "...") {
      pages.push("...");
    }
  }

  return (
    <nav className="flex items-center justify-center gap-1 mt-12" aria-label="分页导航">
      {/* 上一页 */}
      {currentPage > 1 ? (
        <Link
          href={getPageHref(currentPage - 1)}
          className="px-3 py-2 rounded-lg text-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          ← 上一页
        </Link>
      ) : (
        <span className="px-3 py-2 rounded-lg text-sm border border-gray-100 dark:border-gray-800 text-gray-300 dark:text-gray-700 cursor-not-allowed">
          ← 上一页
        </span>
      )}

      {/* 页码 */}
      {pages.map((page, i) =>
        page === "..." ? (
          <span key={`dots-${i}`} className="px-2 py-2 text-sm text-gray-400">
            ...
          </span>
        ) : (
          <Link
            key={page}
            href={getPageHref(page)}
            className={`w-9 h-9 flex items-center justify-center rounded-lg text-sm transition-colors ${
              page === currentPage
                ? "bg-primary-500 text-white font-semibold shadow-sm"
                : "border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
            }`}
          >
            {page}
          </Link>
        )
      )}

      {/* 下一页 */}
      {currentPage < totalPages ? (
        <Link
          href={getPageHref(currentPage + 1)}
          className="px-3 py-2 rounded-lg text-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          下一页 →
        </Link>
      ) : (
        <span className="px-3 py-2 rounded-lg text-sm border border-gray-100 dark:border-gray-800 text-gray-300 dark:text-gray-700 cursor-not-allowed">
          下一页 →
        </span>
      )}
    </nav>
  );
}
