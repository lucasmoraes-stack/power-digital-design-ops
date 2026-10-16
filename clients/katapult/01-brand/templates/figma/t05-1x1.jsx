const imgIpad = "assets/6c5262bb-25a4-47b7-b6f8-60aa291f48c2.png";
const imgVector12 = "assets/135ad3d3-7a8f-4549-8bbc-fdb4a183dd70.svg";
const imgLayer1 = "assets/4adc7cae-b43d-43a5-be30-9b25d2ccd751.svg";

export default function Template05HeroProductBleedCard() {
  return (
    <div className="bg-[#d4a574] relative size-full" data-node-id="547:1106" data-name="template-05-hero-product-bleed-card">
      <div className="absolute h-[1262.636px] left-[-201px] mix-blend-soft-light top-[404px] w-[2429.41px]" data-node-id="547:1107">
        <div className="absolute inset-[-21.23%_-3.12%_-21.23%_0]">
          <img alt="" className="block max-w-none size-full" src={imgVector12} />
        </div>
      </div>
      <div className="absolute h-[828px] left-[83px] top-[474px] w-[576px]" data-node-id="547:1108" data-name="ipad">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[125.14%] left-[-22.14%] max-w-none top-[-12.64%] w-[377.86%]" src={imgIpad} />
        </div>
      </div>
      <div className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Bold'] font-bold leading-[0] left-1/2 not-italic text-[#131540] text-[117.582px] text-center top-[91px] tracking-[-4.7033px] w-[1260.484px]" data-node-id="547:1109">
        <p className="leading-none mb-0">Say yes to the</p>
        <p className="leading-none mb-0">{`thing you've`}</p>
        <p className="leading-none">been eyeing.</p>
      </div>
      <div className="absolute content-stretch flex flex-col gap-[48px] items-center left-[calc(50%+122px)] top-[486px] w-[411px]" data-node-id="547:1110">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[#131540] text-[40px] text-center w-[467px]" data-node-id="547:1111">
          No credit history required. Just a little good karma to spare.
        </p>
        <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1112" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1112;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <p className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-[calc(50%+327.5px)] not-italic text-[#4d4d4d] text-[15px] text-center top-[1098px] w-[347px]" data-node-id="547:1113">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="-translate-x-1/2 -translate-y-1/2 absolute h-[35px] left-[calc(87.5%-114.9px)] top-[calc(50%+451.5px)] w-[157.198px]" data-node-id="547:1114" data-name="Layer_1">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
      </div>
    </div>
  );
}
