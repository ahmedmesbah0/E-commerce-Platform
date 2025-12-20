<?php
/**
 * Product Class
 * Handles product operations
 */

require_once __DIR__ . '/Database.php';

class Product
{
    private $db;

    public function __construct()
    {
        $this->db = Database::getInstance();
    }

    /**
     * Get all products with pagination
     */
    public function getAll($page = 1, $limit = ITEMS_PER_PAGE, $filters = [])
    {
        $offset = ($page - 1) * $limit;
        $conditions = ["p.is_active = 1"];
        $params = [];

        // Apply filters
        if (!empty($filters['category_id'])) {
            $conditions[] = "p.category_id = ?";
            $params[] = $filters['category_id'];
        }

        if (!empty($filters['brand_id'])) {
            $conditions[] = "p.brand_id = ?";
            $params[] = $filters['brand_id'];
        }

        if (!empty($filters['min_price'])) {
            $conditions[] = "p.price >= ?";
            $params[] = $filters['min_price'];
        }

        if (!empty($filters['max_price'])) {
            $conditions[] = "p.price <= ?";
            $params[] = $filters['max_price'];
        }

        if (!empty($filters['search'])) {
            $conditions[] = "(p.name LIKE ? OR p.description LIKE ?)";
            $searchTerm = '%' . $filters['search'] . '%';
            $params[] = $searchTerm;
            $params[] = $searchTerm;
        }

        $where = implode(' AND ', $conditions);

        $sql = "SELECT p.*, c.name as category_name, b.name as brand_name,
                       COALESCE(AVG(r.rating), 0) as avg_rating,
                       COUNT(DISTINCT r.review_id) as review_count,
                       COALESCE(SUM(i.quantity), 0) as stock
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN review r ON p.product_id = r.product_id AND r.is_approved = TRUE
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE {$where}
                GROUP BY p.product_id
                ORDER BY p.created_at DESC
                LIMIT ? OFFSET ?";

        $params[] = $limit;
        $params[] = $offset;

        return $this->db->fetchAll($sql, $params);
    }

    /**
     * Get product by ID
     */
    public function getById($id)
    {
        $sql = "SELECT p.*, c.name as category_name, b.name as brand_name, s.business_name as seller_name,
                       COALESCE(AVG(r.rating), 0) as avg_rating,
                       COUNT(DISTINCT r.review_id) as review_count,
                       COALESCE(SUM(i.quantity), 0) as stock
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN seller s ON p.seller_id = s.seller_id
                LEFT JOIN review r ON p.product_id = r.product_id AND r.is_approved = TRUE
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.product_id = ?
                GROUP BY p.product_id";

        return $this->db->fetchOne($sql, [$id]);
    }

    /**
     * Search products
     */
    public function search($term, $limit = 20)
    {
        $sql = "SELECT p.*, COALESCE(SUM(i.quantity), 0) as stock
                FROM product p
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.is_active = 1 AND (p.name LIKE ? OR p.description LIKE ? OR p.sku LIKE ?)
                GROUP BY p.product_id
                LIMIT ?";

        $searchTerm = '%' . $term . '%';
        return $this->db->fetchAll($sql, [$searchTerm, $searchTerm, $searchTerm, $limit]);
    }

    /**
     * Create new product
     */
    public function create($data)
    {
        $productData = [
            'name' => $data['name'],
            'description' => $data['description'] ?? '',
            'price' => $data['price'],
            'category_id' => $data['category_id'] ?? null,
            'brand_id' => $data['brand_id'] ?? null,
            'seller_id' => $data['seller_id'] ?? null,
            'supplier_id' => $data['supplier_id'] ?? null,
            'sku' => $data['sku'] ?? $this->generateSKU(),
            'weight' => $data['weight'] ?? null,
            'dimensions' => $data['dimensions'] ?? null,
            'is_active' => $data['is_active'] ?? 1
        ];

        return $this->db->insert('product', $productData);
    }

    /**
     * Update product
     */
    public function update($id, $data)
    {
        $allowedFields = [
            'name',
            'description',
            'price',
            'category_id',
            'brand_id',
            'seller_id',
            'supplier_id',
            'sku',
            'weight',
            'dimensions',
            'is_active'
        ];

        $updateData = [];
        foreach ($allowedFields as $field) {
            if (isset($data[$field])) {
                $updateData[$field] = $data[$field];
            }
        }

        return $this->db->update('product', $updateData, 'product_id = ?', [$id]);
    }

    /**
     * Delete product (soft delete)
     */
    public function delete($id)
    {
        return $this->db->update('product', ['is_active' => 0], 'product_id = ?', [$id]);
    }

    /**
     * Get product reviews
     */
    public function getReviews($productId)
    {
        $sql = "SELECT r.*, c.name as customer_name
                FROM review r
                JOIN customer c ON r.customer_id = c.customer_id
                WHERE r.product_id = ? AND r.is_approved = TRUE
                ORDER BY r.created_at DESC";

        return $this->db->fetchAll($sql, [$productId]);
    }

    /**
     * Get related products
     */
    public function getRelated($productId, $limit = 4)
    {
        $product = $this->getById($productId);
        if (!$product)
            return [];

        $sql = "SELECT p.*, COALESCE(AVG(r.rating), 0) as avg_rating
                FROM product p
                LEFT JOIN review r ON p.product_id = r.product_id AND r.is_approved = TRUE
                WHERE p.product_id != ? 
                  AND p.is_active = 1
                  AND (p.category_id = ? OR p.brand_id = ?)
                GROUP BY p.product_id
                ORDER BY RAND()
                LIMIT ?";

        return $this->db->fetchAll($sql, [$productId, $product['category_id'], $product['brand_id'], $limit]);
    }

    /**
     * Get featured products
     */
    public function getFeatured($limit = 8)
    {
        $sql = "SELECT p.*, COALESCE(AVG(r.rating), 0) as avg_rating,
                       COUNT(DISTINCT oi.order_item_id) as sales_count
                FROM product p
                LEFT JOIN review r ON p.product_id = r.product_id AND r.is_approved = TRUE
                LEFT JOIN order_item oi ON p.product_id = oi.product_id
                WHERE p.is_active = 1
                GROUP BY p.product_id
                ORDER BY sales_count DESC, avg_rating DESC
                LIMIT ?";

        return $this->db->fetchAll($sql, [$limit]);
    }

    /**
     * Check stock availability
     */
    public function checkStock($productId, $quantity = 1)
    {
        $sql = "SELECT COALESCE(SUM(quantity), 0) as stock
                FROM inventory
                WHERE product_id = ?";

        $result = $this->db->fetchOne($sql, [$productId]);
        return $result && $result['stock'] >= $quantity;
    }

    /**
     * Generate unique SKU
     */
    private function generateSKU()
    {
        return 'PRD-' . strtoupper(uniqid());
    }

    /**
     * Get total count for pagination
     */
    public function getTotalCount($filters = [])
    {
        $conditions = ["is_active = 1"];
        $params = [];

        if (!empty($filters['category_id'])) {
            $conditions[] = "category_id = ?";
            $params[] = $filters['category_id'];
        }

        if (!empty($filters['brand_id'])) {
            $conditions[] = "brand_id = ?";
            $params[] = $filters['brand_id'];
        }

        if (!empty($filters['search'])) {
            $conditions[] = "(name LIKE ? OR description LIKE ?)";
            $searchTerm = '%' . $filters['search'] . '%';
            $params[] = $searchTerm;
            $params[] = $searchTerm;
        }

        $where = implode(' AND ', $conditions);
        $sql = "SELECT COUNT(*) as count FROM product WHERE {$where}";

        $result = $this->db->fetchOne($sql, $params);
        return $result['count'];
    }
}
