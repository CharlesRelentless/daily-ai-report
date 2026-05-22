/** @type {import('next').NextConfig} */
const nextConfig = {
  // Markdown 文件作为页面内容源
  pageExtensions: ["ts", "tsx", "js", "jsx", "md", "mdx"],

  // 图片允许 AI HOT 等外部源
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**" },
    ],
  },
};

export default nextConfig;
