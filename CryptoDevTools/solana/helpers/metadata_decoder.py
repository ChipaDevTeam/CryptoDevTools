import struct
from typing import Optional, List, Dict, Any
from solders.pubkey import Pubkey

class MetadataDecoder:
    METADATA_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

    @staticmethod
    def get_metadata_pda(mint: Pubkey) -> Pubkey:
        seeds = [
            b"metadata",
            bytes(MetadataDecoder.METADATA_PROGRAM_ID),
            bytes(mint)
        ]
        pda, _ = Pubkey.find_program_address(seeds, MetadataDecoder.METADATA_PROGRAM_ID)
        return pda

    @staticmethod
    def decode_metadata(data: bytes) -> Dict[str, Any]:
        """
        Decodes the raw bytes of a Metaplex Metadata account.
        """
        offset = 0
        
        # 1. Key (u8)
        if len(data) < 1:
             raise ValueError("Data too short")
             
        key = data[0]
        offset += 1
        
        # 2. Update Authority (Pubkey)
        update_authority = Pubkey(data[offset:offset+32])
        offset += 32
        
        # 3. Mint (Pubkey)
        mint = Pubkey(data[offset:offset+32])
        offset += 32
        
        # 4. Data (struct)
        # name (string)
        name_len = struct.unpack("<I", data[offset:offset+4])[0]
        offset += 4
        name = data[offset:offset+name_len].decode("utf-8").strip("\x00")
        offset += name_len
        
        # symbol (string)
        symbol_len = struct.unpack("<I", data[offset:offset+4])[0]
        offset += 4
        symbol = data[offset:offset+symbol_len].decode("utf-8").strip("\x00")
        offset += symbol_len
        
        # uri (string)
        uri_len = struct.unpack("<I", data[offset:offset+4])[0]
        offset += 4
        uri = data[offset:offset+uri_len].decode("utf-8").strip("\x00")
        offset += uri_len
        
        # seller_fee_basis_points (u16)
        seller_fee_basis_points = struct.unpack("<H", data[offset:offset+2])[0]
        offset += 2
        
        # creators (Option<Vec<Creator>>)
        has_creators = data[offset]
        offset += 1
        creators = []
        if has_creators:
            creators_len = struct.unpack("<I", data[offset:offset+4])[0]
            offset += 4
            for _ in range(creators_len):
                creator_address = Pubkey(data[offset:offset+32])
                offset += 32
                verified = bool(data[offset])
                offset += 1
                share = data[offset]
                offset += 1
                creators.append({
                    "address": str(creator_address),
                    "verified": verified,
                    "share": share
                })
        
        # 5. Primary Sale Happened (bool)
        primary_sale_happened = bool(data[offset])
        offset += 1
        
        # 6. Is Mutable (bool)
        is_mutable = bool(data[offset])
        offset += 1
        
        # 7. Edition Nonce (Option<u8>) - Skipping for basic metadata
        
        return {
            "key": key,
            "update_authority": str(update_authority),
            "mint": str(mint),
            "data": {
                "name": name,
                "symbol": symbol,
                "uri": uri,
                "seller_fee_basis_points": seller_fee_basis_points,
                "creators": creators
            },
            "primary_sale_happened": primary_sale_happened,
            "is_mutable": is_mutable
        }
