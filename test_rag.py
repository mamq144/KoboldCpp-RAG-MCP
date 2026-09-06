from server import index_documents, query_knowledge_base

print("=== جاري بدء فهرسة المستندات ===")
index_result = index_documents()
print(index_result)

print("\n=== اختبار البحث والاسترجاع الدلالي ===")
query = "كم هي ميزانية المرحلة الأولى وما هو الرمز التشغيلي؟"
print(f"السؤال: {query}\n")

rag_output = query_knowledge_base(query)
print("النتيجة المسترجعة من قاعدة المتجهات:")
print(rag_output)