const imgIpad = "assets/739ef398-ca54-4160-a5a5-670065ce333b.png";
const imgVector12 = "assets/e6620c11-c063-4366-837c-9a065642ec7a.svg";
const imgLayer1 = "assets/7dc80f51-3568-41b1-9cc4-342161803de2.svg";

export default function Template05HeroProductBleedCard9X16() {
  return (
    <div className="bg-[#d4a574] relative size-full" data-node-id="547:1464" data-name="template-05-hero-product-bleed-card-9x16">
      <div className="absolute h-[1262.636px] left-[-201px] mix-blend-soft-light top-[404px] w-[2429.41px]" data-node-id="547:1465">
        <div className="absolute inset-[-21.23%_-3.12%_-21.23%_0]">
          <img alt="" className="block max-w-none size-full" src={imgVector12} />
        </div>
      </div>
      <div className="absolute h-[1117.8px] left-[151.2px] top-[1094px] w-[777.6px]" data-node-id="547:1466" data-name="ipad">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[125.14%] left-[-22.14%] max-w-none top-[-12.64%] w-[377.86%]" src={imgIpad} />
        </div>
      </div>
      <div className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Bold'] font-bold leading-[0] left-1/2 not-italic text-[#131540] text-[117.582px] text-center top-[280px] tracking-[-4.7033px] w-[1134.435px]" data-node-id="547:1467">
        <p className="leading-none mb-0">Say yes to the</p>
        <p className="leading-none mb-0">{`thing you've`}</p>
        <p className="leading-none">been eyeing.</p>
      </div>
      <div className="absolute content-stretch flex flex-col gap-[48px] items-center left-[calc(25%+64.5px)] top-[642px] w-[411px]" data-node-id="547:1468">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[#131540] text-[40px] text-center w-[467px]" data-node-id="547:1469">
          No credit history required. Just a little good karma to spare.
        </p>
        <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1470" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1470;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <p className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-[calc(25%+270px)] not-italic text-[#4d4d4d] text-[15px] text-center top-[1007px] w-[347px]" data-node-id="547:1471">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="-translate-x-1/2 -translate-y-1/2 absolute h-[35px] left-1/2 top-[calc(50%+19.5px)] w-[157.198px]" data-node-id="547:1472" data-name="Layer_1">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
      </div>
    </div>
  );
}
