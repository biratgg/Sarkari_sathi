from typing import List, Dict, Any, Optional
from vector_store_free import PineconeVectorStoreFree
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGChatbotFree:
    def __init__(self):
        """Initialize RAG Chatbot with free local embeddings"""
        self.config = Config()
        self.vector_store = PineconeVectorStoreFree()
    
    def retrieve_relevant_documents(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for the given query"""
        try:
            relevant_docs = self.vector_store.search_similar(query)
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents")
            return relevant_docs
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")
            return []
    
    def create_context_from_documents(self, documents: List[Dict[str, Any]]) -> str:
        """Create context string from retrieved documents"""
        if not documents:
            return "No relevant information found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}:\n{doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using intelligent rule-based approach"""
        try:
            if "No relevant information found" in context:
                return f"I don't have specific information about '{query}' in my knowledge base. However, I can help you with questions about the topics I do have information about. Try asking about machine learning, Python programming, vector databases, Nepal, or government services."
            
            # Extract relevant information from context
            if len(context) > 0:
                context_lower = context.lower()
                query_lower = query.lower()
                
                # Check for Nepali question patterns first
                if self._is_nepali_query(query_lower):
                    return self._handle_nepali_query(query, context, query_lower)
                
                # Extract specific information based on query type
                if any(word in query_lower for word in ['fee', 'cost', 'price', 'charge', 'शुल्क', 'दस्तुर', 'रकम', 'मूल्य', 'कीमत']):
                    return self._extract_fee_information(context, query)
                elif any(word in query_lower for word in ['document', 'paper', 'कागजात', 'आवश्यक', 'कागज', 'पत्र', 'दस्तावेज']):
                    return self._extract_document_information(context, query)
                elif any(word in query_lower for word in ['process', 'step', 'procedure', 'प्रक्रिया', 'काम', 'कार्य', 'तरिका', 'विधि']):
                    return self._extract_process_information(context, query)
                elif any(word in query_lower for word in ['time', 'duration', 'समय', 'कति', 'कहिले', 'कति बेर', 'अवधि']):
                    return self._extract_time_information(context, query)
                elif any(word in query_lower for word in ['service', 'सेवा', 'available', 'उपलब्ध', 'सुविधा', 'सहायता']):
                    return self._extract_service_information(context, query)
                elif any(word in query_lower for word in ['location', 'where', 'situated', 'position', 'coordinates', 'latitude', 'longitude', 'स्थान', 'कहाँ', 'अवस्थित', 'छ', 'छैन', 'हो', 'हुन्छ']):
                    return self._extract_location_information(context, query)
                elif any(word in query_lower for word in ['nepal', 'नेपाल', 'kathmandu', 'काठमाण्डौ', 'नेपालको', 'नेपालमा', 'नेपाली']):
                    return self._extract_nepal_information(context, query)
                else:
                    return self._extract_general_information(context, query)
            
            return "I found some relevant information, but I'm having trouble processing it right now. Please try rephrasing your question."
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again later."
    
    def _extract_fee_information(self, context: str, query: str) -> str:
        """Extract fee-related information"""
        lines = context.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['fee', 'free', 'निःशुल्क', 'शुल्क', 'दस्तुर']):
                if 'free' in line.lower() or 'निःशुल्क' in line:
                    return f"Based on the information in my knowledge base: **The service is FREE (निःशुल्क)**. There are no charges for this service."
                else:
                    return f"Based on the information in my knowledge base: {line.strip()}"
        return "I couldn't find specific fee information in my knowledge base for this service."
    
    def _extract_document_information(self, context: str, query: str) -> str:
        """Extract document requirements"""
        lines = context.split('\n')
        documents = []
        in_documents_section = False
        
        for line in lines:
            if 'required documents' in line.lower() or 'कागजात' in line:
                in_documents_section = True
                continue
            elif in_documents_section and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                documents.append(line.strip())
            elif in_documents_section and line.strip() and not line.startswith('-'):
                break
        
        if documents:
            response = "Based on my knowledge base, here are the required documents:\n\n"
            for doc in documents:
                response += f"• {doc}\n"
            return response
        return "I couldn't find specific document requirements in my knowledge base."
    
    def _extract_process_information(self, context: str, query: str) -> str:
        """Extract process information"""
        lines = context.split('\n')
        for line in lines:
            if 'process:' in line.lower() or 'प्रक्रिया' in line:
                process_info = line.split(':', 1)[1].strip() if ':' in line else line.strip()
                return f"Based on my knowledge base, here's the process: {process_info}"
        return "I couldn't find specific process information in my knowledge base."
    
    def _extract_time_information(self, context: str, query: str) -> str:
        """Extract time-related information"""
        lines = context.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['time', 'day', 'समय', 'दिन']):
                return f"Based on my knowledge base: {line.strip()}"
        return "I couldn't find specific timing information in my knowledge base."
    
    def _extract_service_information(self, context: str, query: str) -> str:
        """Extract service information"""
        lines = context.split('\n')
        services = []
        for line in lines:
            if 'service' in line.lower() and ':' in line:
                services.append(line.strip())
        
        if services:
            response = "Based on my knowledge base, here are the available services:\n\n"
            for service in services[:3]:  # Limit to first 3 services
                response += f"• {service}\n"
            return response
        return "I couldn't find specific service information in my knowledge base."
    
    def _extract_location_information(self, context: str, query: str) -> str:
        """Extract location-specific information"""
        import re
        
        # Look for location-related patterns
        location_patterns = [
            r'located in ([^.]*)',
            r'situated in ([^.]*)',
            r'position[^.]*?([^.]*)',
            r'coordinates[^.]*?([^.]*)',
            r'latitude[^.]*?([^.]*)',
            r'longitude[^.]*?([^.]*)',
            r'between ([^.]*)',
            r'bordered by ([^.]*)',
            r'neighboring ([^.]*)',
            r'continent[^.]*?([^.]*)',
            r'region[^.]*?([^.]*)'
        ]
        
        location_info = []
        context_lower = context.lower()
        
        for pattern in location_patterns:
            matches = re.findall(pattern, context_lower, re.IGNORECASE)
            for match in matches:
                if match.strip() and len(match.strip()) > 3:
                    location_info.append(match.strip())
        
        # Also look for specific location keywords
        location_keywords = ['asia', 'himalayas', 'himalayan', 'south asia', 'indian subcontinent', 
                           'china', 'india', 'tibet', 'bhutan', 'bangladesh']
        
        for keyword in location_keywords:
            if keyword in context_lower:
                # Find the sentence containing this keyword
                sentences = context.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        location_info.append(sentence.strip())
                        break
        
        if location_info:
            response = "Based on my knowledge base, here's the location information:\n\n"
            for info in location_info[:3]:  # Limit to first 3 location facts
                response += f"• {info}\n"
            return response
        return "I couldn't find specific location information in my knowledge base."
    
    def _extract_nepal_information(self, context: str, query: str) -> str:
        """Extract Nepal-specific information with better filtering"""
        # Extract key facts about Nepal, but be more selective
        lines = context.split('\n')
        nepal_facts = []
        
        # Look for more specific Nepal information
        for line in lines:
            line_lower = line.lower()
            if any(word in line_lower for word in ['nepal', 'kathmandu', 'everest', 'himalaya']):
                # Only include lines that are substantial and relevant
                if len(line.strip()) > 20 and not line.strip().startswith('#'):
                    nepal_facts.append(line.strip())
        
        if nepal_facts:
            response = "Based on my knowledge base, here's what I know about Nepal:\n\n"
            for fact in nepal_facts[:2]:  # Limit to first 2 facts to avoid overload
                response += f"• {fact}\n"
            return response
        return "I couldn't find specific information about Nepal in my knowledge base."
    
    def _is_nepali_query(self, query_lower: str) -> bool:
        """Check if the query contains Nepali text"""
        nepali_chars = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह', 'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ']
        return any(char in query_lower for char in nepali_chars)
    
    def _handle_nepali_query(self, query: str, context: str, query_lower: str) -> str:
        """Handle Nepali language queries with better understanding"""
        # Common Nepali question words
        question_words = {
            'कहाँ': 'location',
            'कहिले': 'time', 
            'कति': 'amount/time',
            'कसरी': 'process',
            'कुन': 'which',
            'के': 'what',
            'किन': 'why',
            'कसले': 'who'
        }
        
        # Detect question type based on Nepali question words
        detected_type = None
        for word, q_type in question_words.items():
            if word in query_lower:
                detected_type = q_type
                break
        
        # Map to appropriate extraction method
        if detected_type == 'location' or any(word in query_lower for word in ['स्थान', 'छ', 'छैन']):
            return self._extract_location_information(context, query)
        elif detected_type == 'time' or any(word in query_lower for word in ['समय', 'बेर', 'अवधि']):
            return self._extract_time_information(context, query)
        elif detected_type == 'amount' or any(word in query_lower for word in ['शुल्क', 'रकम', 'मूल्य']):
            return self._extract_fee_information(context, query)
        elif detected_type == 'process' or any(word in query_lower for word in ['प्रक्रिया', 'तरिका', 'विधि']):
            return self._extract_process_information(context, query)
        elif any(word in query_lower for word in ['सेवा', 'सुविधा', 'सहायता']):
            return self._extract_service_information(context, query)
        elif any(word in query_lower for word in ['कागजात', 'कागज', 'पत्र']):
            return self._extract_document_information(context, query)
        elif any(word in query_lower for word in ['नेपाल', 'काठमाण्डौ', 'नेपाली']):
            return self._extract_nepal_information(context, query)
        else:
            # General Nepali response
            return self._extract_general_information(context, query)
    
    def _extract_general_information(self, context: str, query: str) -> str:
        """Extract general information"""
        lines = context.split('\n')
        relevant_info = []
        
        for line in lines:
            if line.strip() and not line.startswith('Document') and len(line.strip()) > 20:
                relevant_info.append(line.strip())
        
        if relevant_info:
            response = "Based on my knowledge base, here's what I found:\n\n"
            for info in relevant_info[:2]:  # Limit to first 2 relevant pieces
                response += f"• {info}\n"
            return response
        return "I found some relevant information, but I'm having trouble processing it right now. Please try rephrasing your question."
    
    def chat(self, query: str) -> Dict[str, Any]:
        """Main chat function that implements RAG pipeline"""
        try:
            # Step 0: Preprocess query for better multilingual support
            processed_query = self._preprocess_query(query)
            
            # Step 1: Retrieve relevant documents
            relevant_docs = self.retrieve_relevant_documents(processed_query)
            
            # Step 2: Create context from documents
            context = self.create_context_from_documents(relevant_docs)
            
            # Step 3: Generate response using context
            response = self.generate_response(query, context)
            
            # Step 4: Return response with metadata
            return {
                'response': response,
                'relevant_documents': relevant_docs,
                'context_used': len(relevant_docs) > 0,
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Error in chat function: {e}")
            return {
                'response': "I apologize, but I encountered an error while processing your request. Please try again.",
                'relevant_documents': [],
                'context_used': False,
                'query': query,
                'error': str(e)
            }
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess query for better multilingual support"""
        # Add common English translations for Nepali terms
        nepali_english_map = {
            'कहाँ': 'where location',
            'कहिले': 'when time',
            'कति': 'how much amount',
            'कसरी': 'how process',
            'के': 'what',
            'किन': 'why',
            'कसले': 'who',
            'नेपाल': 'nepal',
            'काठमाण्डौ': 'kathmandu',
            'सेवा': 'service',
            'कागजात': 'document',
            'शुल्क': 'fee cost',
            'समय': 'time',
            'प्रक्रिया': 'process'
        }
        
        processed_query = query
        for nepali, english in nepali_english_map.items():
            if nepali in query.lower():
                processed_query += f" {english}"
        
        return processed_query
    
    def add_knowledge(self, documents: List[Dict[str, Any]]) -> bool:
        """Add new knowledge to the vector store"""
        try:
            success = self.vector_store.add_documents(documents)
            if success:
                logger.info(f"Successfully added {len(documents)} documents to knowledge base")
            return success
        except Exception as e:
            logger.error(f"Failed to add knowledge: {e}")
            return False
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            return self.vector_store.get_index_stats()
        except Exception as e:
            logger.error(f"Failed to get knowledge stats: {e}")
            return {}
    
    def clear_knowledge_base(self) -> bool:
        """Clear all documents from the knowledge base"""
        try:
            # This would require deleting all vectors from the index
            # For now, we'll return False as this is a destructive operation
            logger.warning("Clear knowledge base operation not implemented for safety")
            return False
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            return False
